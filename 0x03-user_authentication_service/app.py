#!/usr/bin/env python3
"""User authentication service module using Flask.
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """This route handles the root endpoint.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """This route handles the creation of new users.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "User created"})
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400


@app.route('/sessions', methods=['POST'])
@app.route('/login', methods=['POST'])
def login() -> str:
    """This route handles user login and session creation.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    user = AUTH.valid_login(email, password)
    if user:
        session_id = AUTH.create_session(user.id)
        response = jsonify({"email": user.email, "message": "Logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """This route handles user logout and session destruction.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """This route handles retrieving the user's profile information.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """This route handles generating a reset password token for a user.
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """This route handles updating the user's password using a reset password token.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
