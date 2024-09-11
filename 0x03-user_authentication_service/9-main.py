#!/usr/bin/env python3
"""
9-Main file - 13. Destroy user session
"""
from auth import Auth
from user import User


def main():
    # Initialize the Auth instance
    auth = Auth()

    # Define test email and password
    email = 'testuser1@example.com'
    password = 'TestPassword123'

    # Register a new user
    auth.register_user(email, password)

    # Create a session for the user
    session_id = auth.create_session(email)
    # session_id = "f5867204-9168-46eb-83e4-56f3e2839e4c"

    # Retrieve user by session ID
    user = auth.get_user_from_session_id(session_id)

    if user:
        print(
            f"User before destroying session: {user.email}, Session ID: {user.session_id}")

    # Destroy the session
    auth.destroy_session(user.id)

    # Retrieve user again to check if session ID is None
    user = auth.get_user_from_session_id(session_id)

    if user:
        print(
            f"User after destroying session: {user.email}, Session ID: {user.session_id}")
    else:
        print("Session destroyed successfully, user not found with the old session ID")


if __name__ == "__main__":
    main()
