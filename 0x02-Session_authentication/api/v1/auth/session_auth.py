#!/usr/bin/env python3
""" Module of session authentication
"""
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import uuid
from api.v1.views import app_views
from flask import request, jsonify
import os



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
        print(SessionAuth.user_id_by_session_id)
        if user_id:
            return user_id
        return None

    def current_user(self, request=None):
        """returns a User instance based on a cookie value:"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes = False)
def login():
    """login handler"""
    email = request.form.get('email')
    if not email:
        return  { "error": "email missing" }, 400
    password = request.form.get('password')
    if not password:
        return  { "error": "password missing" }, 400
    User.load_from_file()
    users = User.search({"email": email})
    if users is None:
        return { "error": "no user found for this email" }, 404
    for user in users:
        if not user.is_valid_password(password):
            return { "error": "wrong password" }, 401
        else:
            from api.v1.app import auth
            user_id = user.id
            session_id = auth.create_session(user_id)
            cookie_name =os.getenv('SESSION_NAME')
            out = jsonify(user.to_json())
            out.set_cookie(cookie_name, session_id)
            return out