#!/usr/bin/env python3
"""
Basic Flask app with user registration endpoint.
"""
from flask import Flask, request, redirect, jsonify, abort, make_response
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
    return (response)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ Log out the user by destroying the session. """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
        AUTH.destroy_session(user.id)
    return redirect('/')@app.route('/profile', methods=['GET'])


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Retrieve the user's profile using the session_id cookie."""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return (jsonify({"message": "session_id cookie is missing"}), 403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return (jsonify({"message": "session_id user not found"}), 403)

    return jsonify({"email": user.email})@app.route('/reset_password',
                                                    methods=['POST'])


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ Generate and return a reset password token for the given email. """
    email = request.form.get('email')
    if not email:
        abort(400, description="Email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403, description="Email not registered")
    response = jsonify({"email": email, "reset_token": reset_token})
    return (response, 200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
