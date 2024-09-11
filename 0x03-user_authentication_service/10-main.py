#!/usr/bin/env python3
"""
10-Main file - 14. Log out user.
"""
import requests
from auth import Auth
from user import User


def main():
    # Define test email and password
    email = 'testuser@example.com'
    password = 'TestPassword123'

    # Register a new user
    auth = Auth()
    auth.register_user(email, password)

    # Create a session for the user
    session_id = auth.create_session(email)
    if session_id:
        print(f"Session ID created: {session_id}")
    else:
        print("Failed to create session.")

    # Retrieve user by session ID
    user = auth.get_user_from_session_id(session_id)
    if user:
        print(f"User found: {user.email}")
    else:
        print("No user found with the given session ID")

    # Log out the user by deleting the session
    response = requests.delete(
        'http://localhost:5000/sessions',
        cookies={'session_id': session_id}
    )

    # Print the response status code
    print(f"User: {user.email} logged out")
    print(f"Logout response status code: {response.status_code}")

    # Print the response text if any
    print(f"Response text: {response.text}")


if __name__ == "__main__":
    main()
