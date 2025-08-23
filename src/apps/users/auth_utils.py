from argon2 import PasswordHasher

hasher = PasswordHasher()

def hash_password(password: str) -> bytes:
    """Hashes a password using argon2 algorithm"""
    password = bytes(password)

    hashed = hasher.hash(password).encode("utf-8")
    return hashed