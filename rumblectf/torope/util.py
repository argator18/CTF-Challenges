import os
import base64
import json

from dataclasses import is_dataclass, fields
from typing import Any

from Crypto.Hash import SHA3_256
from Crypto.Cipher import AES


def encode_complex(obj):
    """Encode dataclasses and bytes into JSON-friendly structures."""
    if is_dataclass(obj):
        return {f.name: encode_complex(getattr(obj, f.name)) for f in fields(obj)}
    elif isinstance(obj, bytes):
        # Prefix byte data to distinguish it
        return 'BASE64:' + base64.b64encode(obj).decode()
    elif isinstance(obj, list):
        return [encode_complex(item) for item in obj]
    return obj

def decode_complex(cls, obj):
    """Recursively decode dictionaries into dataclasses and specially marked base64 strings into bytes."""
    if is_dataclass(cls) and isinstance(obj, dict):  # Ensure that the object is a dictionary and cls is a dataclass
        field_types = {f.name: f.type for f in fields(cls)}
        # Construct a new instance by recursively decoding each field
        return cls(**{f: decode_complex(field_types[f], obj[f]) for f in obj if f in obj and f in field_types})
    elif isinstance(obj, str) and obj.startswith('BASE64:'):
        # Decode the base64 encoded string
        return base64.b64decode(obj[7:])
    elif isinstance(obj, list):
        # Check if the list's elements are dataclass types or need byte decoding
        return [decode_complex(None, item) for item in obj]
    return obj

def serialize_dataclass(instance: Any) -> bytes:
    enc = json.dumps(encode_complex(instance)).encode()
    return enc

def deserialize_dataclass(cls: object, data: bytes) -> Any:
    dec = decode_complex(cls, json.loads(data))
    return dec

def kdf(x: bytes) -> bytes:
    h = SHA3_256.new()
    h.update(b"PMS")
    h.update(x)
    return h.digest()

def decrypt_message(key:bytes, ciphertext: bytes, seq: int) -> bytes:
    nonce, ciphertext, tag = ciphertext[:12], ciphertext[12:-16], ciphertext[-16:]

    aes = AES.new(key, nonce=nonce, mode=AES.MODE_GCM)
    aes.update(seq.to_bytes(4, 'little'))

    try:
        return aes.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print(f'decryption error')
        exit(1)

def encrypt_message(key: bytes, plaintext: bytes, seq: int) -> bytes:
    nonce = os.urandom(12)

    aes = AES.new(key, nonce=nonce, mode=AES.MODE_GCM)
    aes.update(seq.to_bytes(4, 'little'))

    ciphertext, tag = aes.encrypt_and_digest(plaintext)

    return nonce + ciphertext + tag

