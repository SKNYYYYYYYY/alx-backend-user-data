#!/usr/bin/env python3
"""Module to add an expiration date to a session id
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import os


class SessionExpAuth(SessionAuth):
    """handle session id expiration"""
    def __init__(self):
        """constructor"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overloaded method"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get the user id"""
        if session_id is None:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if not user_id:
            return None
        if self.session_duration <= 0:
            return self.session_dict['user_id']
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        created_at = self.user_id_by_session_id[session_id]['created_at']
        duration = timedelta(seconds=self.session_duration)
        if datetime.now() > (created_at + duration):
            return None
        return self.user_id_by_session_id[session_id].get("user_id")
