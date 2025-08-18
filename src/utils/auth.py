from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerificationError, VerifyMismatchError

from src.config.settings import env

ph = PasswordHasher(
    time_cost=env.PASSWORD_HASH_TIME_COST,
    memory_cost=env.PASSWORD_HASH_MEMORY_COST,
    parallelism=env.PASSWORD_HASH_PARALLELISM,
    hash_len=env.PASSWORD_HASH_LENGTH,
    salt_len=env.PASSWORD_HASH_SALT_LENGTH,
)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using Argon2.
    
    :param password: The plaintext password.
    :return: The Argon2 hash string.
    """
    return ph.hash(password)


def verify_password(hash_: str, password: str) -> bool:
    """
    Verify a plaintext password against an Argon2 hash.

    :param hash_: The stored Argon2 hash.
    :param password: The plaintext password to verify.
    :return: True if the password matches, False otherwise.
    """
    try:
        return ph.verify(hash_, password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
