import os

from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Signature import eddsa
from Crypto.Cipher import AES

from util import serialize_dataclass, deserialize_dataclass, encrypt_message, decrypt_message, kdf
from messages import Message, ClientHello, ServerHello, AuthenticationRequest, ServiceSelection, StartService, PlantFlag

class Server:
    def __init__(self, signature_key: ECC.EccKey, password: str):
        self.signature_key = signature_key
        self.send_seq = 0
        self.recv_seq = 0
        self.user = {'admin': password, 'user': os.urandom(32).hex()}
        self.authenticated_user = None
        self.handshake_complete = False

        print(f'user password: {self.user["user"]}')

    def handle_message(self, msg: bytes) -> bytes:
        self.recv_seq += 1
        if hasattr(self, 'pms'):
            msg = decrypt_message(self.pms, msg, self.recv_seq)
        message = deserialize_dataclass(Message, msg)

        match message.type:
            case 1:
                resp = self.handle_client_hello(msg)
                self.send_seq += 1
                return [serialize_dataclass(resp[0])]
            case 3:
                resp = self.handle_authentication_request(msg)
            case 4:
                resp = self.handle_service_selection(msg)
            case 6:
                resp = self.handle_plant_flag(msg)
            case _:
                return []

        for i in range(len(resp)):
            self.send_seq += 1
            resp[i] = serialize_dataclass(resp[i])
            if self.pms:
                resp[i] = encrypt_message(self.pms, resp[i], self.send_seq)
        return resp

    def handle_client_hello(self, msg: bytes):
        ch: ClientHello = deserialize_dataclass(ClientHello, msg)

        self.ephemeral_key = ECC.generate(curve='p256')

        eph_pk = ECC.import_key(encoded=ch.ephemeral_pk, curve_name='p256')
        self.pms = key_agreement(eph_priv=self.ephemeral_key, eph_pub=eph_pk, kdf=kdf)

        eph_pk = self.ephemeral_key.public_key().export_key(format='raw')
        sig_key = eddsa.new(self.signature_key, 'rfc8032')

        sig = sig_key.sign(ch.ephemeral_pk + eph_pk)

        self.handshake_complete = True

        return [ServerHello(type=2, ephemeral_pk=eph_pk, signature=sig)]

    def handle_authentication_request(self, msg: bytes):
        ar: AuthenticationRequest = deserialize_dataclass(AuthenticationRequest, msg)

        if ar.username in self.user and ar.password == self.user[ar.username]:
            self.authenticated_user = ar.username
        else:
            self.authenticated_user = None

        return []

    def handle_service_selection(self, msg: bytes):
        ss: ServiceSelection = deserialize_dataclass(ServiceSelection, msg)

        if self.authenticated_user is None or not self.handshake_complete:
            return []

        return [StartService(type=5, success=True)]


    def handle_plant_flag(self, msg: bytes):
        pf: PlantFlag = deserialize_dataclass(PlantFlag, msg)

        if self.authenticated_user is None or not self.handshake_complete:
            return []

        nonce = os.urandom(12)
        aes = AES.new(bytes.fromhex(self.user[self.authenticated_user]), nonce=nonce, mode=AES.MODE_CTR)
        c = nonce + aes.encrypt(pf.flag.encode())
        print(nonce,c)
        print(f"Flag has been planted: {c.hex()}")

        exit(0)

