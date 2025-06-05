#!/usr/bin/env python3
"""Hashing module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """uses bcrypt to hash a password"""
    return bcrypt.hashpw(bytes(password, 'UTF-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate unique ID"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """validates credetials"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(bytes(password, 'UTF-8'), user.hashed_password):
                return True
            return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """return session id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """returns a user based on a session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroys a session"""
        try:
            if user_id is None:
                return None
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token (self, email: str) -> str:
        """gernerates a UUID as reset token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
