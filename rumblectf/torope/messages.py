from dataclasses import dataclass

@dataclass
class Message:
    type: int

@dataclass
class ClientHello(Message): # Type: 1
    ephemeral_pk: bytes

@dataclass
class ServerHello(Message): # Type: 2
    ephemeral_pk: bytes
    signature: bytes

@dataclass
class AuthenticationRequest(Message): # Type: 3
    username: str
    password: str

@dataclass
class ServiceSelection(Message): # Type: 4
    service: str

@dataclass
class StartService(Message): # Type: 5
    success: bool

@dataclass
class PlantFlag(Message): # Type: 6
    flag: str

