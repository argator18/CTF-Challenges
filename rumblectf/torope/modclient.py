import os

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
from Crypto.Protocol.DH import key_agreement

from util import deserialize_dataclass, serialize_dataclass, decrypt_message, encrypt_message, kdf
from messages import Message, ClientHello, ServerHello, AuthenticationRequest, ServiceSelection, StartService, PlantFlag

class Client:
    def __init__(self,password: str):
        self.password = password
        self.send_seq = 0
        self.recv_seq = 0
        self.handshake_complete = False

    def generate_initial_message(self):
        self.ephemeral_key = ECC.generate(curve='p256')

        ch = ClientHello(type=1, ephemeral_pk=self.ephemeral_key.public_key().export_key(format='raw'))

        self.send_seq += 1
        return serialize_dataclass([serialize_dataclass(ch)])
    
    def encrypt_message(self, msg: bytes) -> bytes:
        self.send_seq += 1
        print(self.send_seq)
        return serialize_dataclass([encrypt_message(self.pms, msg, self.send_seq)])
    
    def increase_seq(self, seq):
        self.send_seq += seq

    def create_server_auth(self):
        return serialize_dataclass([serialize_dataclass(AuthenticationRequest(type=3, username="user", password=self.password))])


    def handle_message(self, msg: bytes) -> bytes:
        self.recv_seq += 1
        if hasattr(self, 'pms'):
            msg = decrypt_message(self.pms, msg, self.recv_seq)
        message = deserialize_dataclass(Message, msg)

        match message.type:
            case 2:
                resp = self.handle_server_hello(msg)
            case 5:
                resp = self.handle_start_service(msg)
            case _:
                return []

        for i in range(len(resp)):
            self.send_seq += 1
            resp[i] = serialize_dataclass(resp[i])
            if self.pms:
                resp[i] = encrypt_message(self.pms, resp[i], self.send_seq)
        return serialize_dataclass(resp)

    def handle_server_hello(self, msg):
        sh: ServerHello = deserialize_dataclass(ServerHello, msg)

        eph_pk = ECC.import_key(encoded=sh.ephemeral_pk, curve_name='p256')
        self.pms = key_agreement(eph_priv=self.ephemeral_key, eph_pub=eph_pk, kdf=kdf)

        self.handshake_complete = True

        return [AuthenticationRequest(type=3, username="user", password=self.password)]

    def decrypt_flag(flag_hex):
        c = bytes.fromhex(flag_hex)
        nonce = c[:12]
        flag = c[12:]
        aes = AES.new(bytes.fromhex(self.password), nonce=nonce, mode=AES.MODE_CTR)
        return aes.decrypt()

