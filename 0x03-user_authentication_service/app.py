#!/usr/bin/env python3
"""
Basic Flask app with user registration endpoint.
"""
from flask import Flask, request, jsonify, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

# Home route for welcome message


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """ Returns a JSON response with a welcome message. """
    return (jsonify({"message": "Bienvenue"}), 200)

# User registration route


@app.route('/users', methods=['POST'])
def register_user():
    """
    Registers a new user via POST request with 'email'
    and 'password' form data.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return (jsonify({"email": user.email, "message": "user created"}), 200)
    except ValueError:
        return (jsonify({"message": "email already registered"}), 400)


@app.route('/sessions', methods=['POST'])
def login():
    """
    POST /sessions route to log in a user.
    Expects form data with 'email' and 'password'.
    If login is successful, returns JSON response with email and message.
    If login fails, returns 401 Unauthorized.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # validation and session creation
    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    # set the session ID in a cookie and return response
    response = make_response(
        jsonify({"email": email, "message": "logged in"}))
    # jsonify({"email": email, "message": f"user {email} logged in"}))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
