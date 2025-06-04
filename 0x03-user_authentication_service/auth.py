#!/usr/bin/env python3
"""Hashing module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """uses bcrypt to hash a password"""
    return bcrypt.hashpw(bytes(password, 'UTF-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with authentication database"""
    def __init__(self):
        """constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user in the db"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = User()
            hashed_pwd = _hash_password(password=password)
            self._db.add_user(email, hashed_pwd)
            self._db._DB__session.commit()
            return user
