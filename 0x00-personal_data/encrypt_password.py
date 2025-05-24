#!/usr/bin/env python3
"""password hasher"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password for the first time, with a randomly-generated salt"""
    hashed = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    return hashed
