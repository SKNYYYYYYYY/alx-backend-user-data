#!/usr/bin/env python3
""" Module of session authentication
"""
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import uuid


class SessionAuth(Auth):
    """handles Session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """session creator"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        if user_id:
            return user_id
        return None

    def current_user(self, request=None):
        """returns a User instance based on a cookie value:"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """deletes session id"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_by_session_id is None:
            return False
        else:
            if session_id not in self.user_id_by_session_id:
                return False
            del self.user_id_by_session_id[session_id]
        return True
