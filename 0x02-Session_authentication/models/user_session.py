#!/usr/bin/env python3
"""Module to save session id in file
"""
from models.base import Base


class UserSession(Base):
    """saves session id"""
    def __init__(self, *args, **kwargs):
        """initialize usersession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def create_session(self, user_id=None):
        """creates and store session instance"""
        user = UserSession()
        
