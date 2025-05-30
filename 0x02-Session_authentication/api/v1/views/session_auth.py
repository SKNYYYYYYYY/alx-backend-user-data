#!/usr/bin/env python3
""" Module of session authentication
"""
from api.v1.views import app_views
from flask import request, abort, jsonify
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login handler"""
    email = request.form.get('email')
    if not email:
        return {"error": "email missing"}, 400
    password = request.form.get('password')
    if not password:
        return {"error": "password missing"}, 400
    User.load_from_file()
    users = User.search({"email": email})
    if users is None:
        return {"error": "no user found for this email"}, 404
    for user in users:
        if not user.is_valid_password(password):
            return {"error": "wrong password"}, 401
        else:
            from api.v1.app import auth
            user_id = user.id
            session_id = auth.create_session(user_id)
            cookie_name = os.getenv('SESSION_NAME')
            out = jsonify(user.to_json())
            out.set_cookie(cookie_name, session_id)
            return out

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """login handler"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    else:
        return jsonify({}), 200
