#!/usr/bin/env python3
"""
Basic Flask app with user registration endpoint.
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

# Home route for welcome message


@app.route('/', methods=['GET'])
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
