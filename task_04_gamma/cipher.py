import hashlib
import json
import random


def apply_gamma(data: bytes, salt: str) -> bytes:
    if not isinstance(salt, str) or not salt:
        raise ValueError("Соль должна быть непустой строкой.")
    generator = random.Random(salt)
    return bytes(value ^ generator.getrandbits(8) for value in data)


def checksum(data: bytes, salt: str, encoding: str) -> str:
    metadata = json.dumps([salt, encoding], ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(metadata + b"\n" + data).hexdigest()
