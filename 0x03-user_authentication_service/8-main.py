#!/usr/bin/env python3
"""
8-Main file - 12. Find user by session ID.
"""
from auth import Auth
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def main():
    # Initialize the Auth instance
    auth = Auth()

    # Define test email and password
    email = 'testuser@example.com'
    password = 'TestPassword123'

    # Register a new user
    try:
        auth.register_user(email, password)
    except ValueError as e:
        print(f"Error: {e}")

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

    # Test with a non-existing session ID
    non_existing_session_id = str(uuid.uuid4())  # Generate a new random UUID
    user = auth.get_user_from_session_id(non_existing_session_id)
    if user:
        print(f"User found with non-existing session ID: {user.email}")
    else:
        print("No user found with the non-existing session ID")

    # Test with None as session ID
    user = auth.get_user_from_session_id(None)
    if user:
        print(f"User found with None as session ID: {user.email}")
    else:
        print("No user found with None as session ID")


if __name__ == "__main__":
    main()
