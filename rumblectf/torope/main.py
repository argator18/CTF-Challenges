import os
import json

from typing import List

from Crypto.PublicKey import ECC

from server import Server
from client import Client
from util import decode_complex, encode_complex, serialize_dataclass, deserialize_dataclass


def main():
    static_key = ECC.generate(curve='ed25519')
    password = os.urandom(32).hex()

    client = Client(static_key.public_key(), password);
    server = Server(static_key, password)

    initial_message = client.generate_initial_message()
    initial_message = serialize_dataclass([serialize_dataclass(initial_message)])
    initial_message = initial_message.hex()
    print(f"Initial client message: {initial_message}")

    while True:
        option = input("To whom do you want to send a message?> ").strip()
        msgs: str = input("Msg> ").strip()

        msgs = bytes.fromhex(msgs).decode()
        msgs = deserialize_dataclass(None, msgs)

        resp = []
        match option[0]:
            case "s":
                for msg in msgs:
                    resp.extend(server.handle_message(msg))
            case "c":
                for msg in msgs:
                    resp.extend(client.handle_message(msg))
            case _:
                continue

        resp = serialize_dataclass(resp)
        resp = resp.hex()
        print(f"Response: {resp}")


if __name__ == '__main__':
    main()
