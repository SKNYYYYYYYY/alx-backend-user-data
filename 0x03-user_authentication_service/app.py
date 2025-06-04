#!/usr/bin/env python3
"""flask app module
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


app = Flask(__name__)

AUTH = Auth()

@app.get("/")
def home():
    """home endpoint"""
    msg = {"message":"Bienvenue"}
    return jsonify(msg)

@app.post("/users")
def users():
    """register new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message":"user created"})
    except Exception:
        return jsonify({"message":"email already registered"}), 400

@app.post("/sessions")
def login():
    """login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email=email, password=password):
        abort(401)

    session_id = AUTH.create_session(email=email)

    response = make_response(jsonify({"email": email, "message":"logged in"}))
    response.set_cookie("session_id", session_id)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")