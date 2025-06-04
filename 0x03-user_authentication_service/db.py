#!/usr/bin/env python3
"""Database module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
import bcrypt


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """constructor"""
        self._engine = create_engine('sqlite:///a.db', echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save a user to the db"""
        user = User(email=email, hashed_password=hashed_password)
        self._session
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs):
        """returns a user from the db"""
        self._session
        for key, val in kwargs.items():
            try:
                getattr(User, key)
            except Exception:
                raise InvalidRequestError
            user = self.__session.query(User).filter(getattr(User, key) == val)
            if user.count() == 0:
                raise NoResultFound
            return user.first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """update the user"""
        user = DB.find_user_by(self, id=user_id)
        for key, val in kwargs.items():
            try:
                getattr(user, key)
            except Exception:
                raise ValueError
            setattr(user, key, val)
        return None
