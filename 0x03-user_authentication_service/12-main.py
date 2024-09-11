#!/usr/bin/env python3
"""
12-Main file - 16. Generate reset password token.
"""
from auth import Auth


def main():
    auth = Auth()

    email = 'test@example.com'
    password = 'SecurePassword123'

    # Assuming you have a method to register a user
    try:
        auth.register_user(email, password)
    except Exception as e:
        print(f"Error registering user: {e}")

    try:
        reset_token = auth.get_reset_password_token(email)
        print(f"Reset token for {email}: {reset_token}")
    except ValueError as e:
        print(f"Error: {e}")

    # Invalid user
    try:
        reset_token = auth.get_reset_password_token(password)
        print(f"Reset token for {email}: {reset_token}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
