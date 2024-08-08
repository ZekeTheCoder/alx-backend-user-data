#!/usr/bin/env python3
""" Module for Session Authentication Views"""
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /api/v1/auth_session/login
    Handle POST request to login and create a session for the user.
    Retrieves email and password from request, verify user, and create session.

    Returns:
        str: JSON response with user data or error message.
    """
    # Email and Password Extraction with default empty string and Validation
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        # find users based on the email.
        users = User.search({'email': email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404

        for user in users:
            # Password Verification
            if user.is_valid_password(password):
                from api.v1.app import auth

                # Create session
                session_id = auth.create_session(user.id)
                if not session_id:
                    return jsonify({"error": "session creation failed"}), 500

                # Create the response(dictionary representation of the User)
                response = jsonify(user.to_json())

                # Set the session cookie
                response.set_cookie(getenv('SESSION_NAME'), session_id)

                return response

        return jsonify({"error": "wrong password"}), 401

    # Catches any exceptions and returns a 500 error with exception message.
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # server error with message


@app_views.route('/auth_session/logout', methods=['DELETE'])
def logout():
    """
    Handles the logout request by removing the user session.

    Returns:
        : A JSON response with an empty dictionary and status code 200
        on success, otherwise an error response with status code 404.
    """
    from api.v1.app import auth

    # Attempt to destroy the session using the auth object
    if not auth.destroy_session(request):
        abort(404)

    # Return an empty JSON response indicating successful logout
    return jsonify({}), 200
