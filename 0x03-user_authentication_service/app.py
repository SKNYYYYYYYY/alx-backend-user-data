#!/usr/bin/env python3
"""flask app module
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from db import DB


app = Flask(__name__)

AUTH = Auth()
mydb = DB()


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
    else:
        response = make_response()
        response.status_code = 403
        return response


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    email = request.form.get("email")
    try:
        user = mydb.find_user_by(email=email)
    except Exception:
        response = make_response()
        response.status_code = 403
        return response
    reset_token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"])
def update_password():
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_pwd = request.form.get("new_password")
    try:
        ret = AUTH.update_password(reset_token=reset_token, password=new_pwd)
        if ret is None:
            msg = {"email": email, "message": "Password updated"}
            return jsonify(msg), 200
    except Exception as e:
        print("errr", e)
        response = make_response()
        response.status_code = 403
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
