#!/usr/bin/env python3
"""Password Encryption and Validation
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Encrypts the given password using bcrypt hashing algorithm.

    Args:
        password (str): The password to be encrypted.

    Returns:
        bytes: The encrypted password.
    """
    encoded_password = password.encode()
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password by comparing it with a hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    encoded_password = password.encode()
    return bcrypt.checkpw(encoded_password, hashed_password)
