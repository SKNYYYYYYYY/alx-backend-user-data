#!/usr/bin/env python3
"""password hasher"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password for the first time, with a randomly-generated salt"""
    hashed = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if password is valid"""
    if (bcrypt.checkpw(bytes(password, "UTF-8"), hashed_password)):
        return True
    return False
