#!/usr/bin/env python3
"""flask app module
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """home endpoint"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route("/users", methods=["POST"])
def users():
    """register new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email=email, password=password):
        abort(401)

    session_id = AUTH.create_session(email=email)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_session(user_id=user.id)
        return redirect("/")
    else:
        response = make_response()
        response.status_code = 403
        return response


@app.route("/profile", methods=['GET'])
def profile():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
