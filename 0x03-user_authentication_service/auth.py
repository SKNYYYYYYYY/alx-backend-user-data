#!/usr/bin/env python3
"""Hashing module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound




class Auth:
    """Auth class to interact with authentication database"""

    def __init__(self):
        """constructor"""
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """uses bcrypt to hash a password"""
        return str(bcrypt.hashpw(bytes(password, 'UTF-8'), bcrypt.gensalt()))

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

    def valid_login(self, email: str, password: str) -> bool:
        """validates credetials"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(bytes(password, 'UTF-8'), user.hashed_password):
                return True
            return False
        except Exception as e:
            return False

    def _generate_uuid(self) -> str:
        """generate unique ID"""
        return uuid.uuid4()

    def create_session(self, email: str) -> str:
        """return session id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(Auth._generate_uuid(self))
            user.session_id = str(session_id)
            self._db._DB__session.commit()
            return session_id
        except Exception as e:
            return None
