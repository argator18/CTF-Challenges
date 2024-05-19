import os

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
from Crypto.Protocol.DH import key_agreement

from util import deserialize_dataclass, serialize_dataclass, decrypt_message, encrypt_message, kdf
from messages import Message, ClientHello, ServerHello, AuthenticationRequest, ServiceSelection, StartService, PlantFlag

class Client:
    def __init__(self, server_pk: ECC.EccKey, password: str):
        self.server_pk = server_pk
        self.password = password
        self.send_seq = 0
        self.recv_seq = 0
        self.handshake_complete = False

    def generate_initial_message(self):
        self.ephemeral_key = ECC.generate(curve='p256')

        ch = ClientHello(type=1, ephemeral_pk=self.ephemeral_key.public_key().export_key(format='raw'))

        self.send_seq += 1
        return ch

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
        return resp

    def handle_server_hello(self, msg):
        sh: ServerHello = deserialize_dataclass(ServerHello, msg)

        try:
            eph_pk = self.ephemeral_key.public_key().export_key(format='raw')
            vrf_key = eddsa.new(self.server_pk, 'rfc8032')
            vrf_key.verify(eph_pk + sh.ephemeral_pk, sh.signature)
        except ValueError:
            exit(1)

        eph_pk = ECC.import_key(encoded=sh.ephemeral_pk, curve_name='p256')
        self.pms = key_agreement(eph_priv=self.ephemeral_key, eph_pub=eph_pk, kdf=kdf)

        self.handshake_complete = True

        return [AuthenticationRequest(type=3, username="admin", password=self.password), ServiceSelection(type=4, service='Flag')]

    def handle_start_service(self, msg: bytes):
        ar: StartService = deserialize_dataclass(StartService, msg)

        if ar.success and self.handshake_complete:
            return [PlantFlag(type=6, flag=os.environ['FLAG'])]

        return []
