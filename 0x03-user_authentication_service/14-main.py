#!/usr/bin/env python3
"""
14-Main file - 18. Update password
"""
from auth import Auth


def main():
    # Initialize Auth instance
    auth = Auth()

    # Register a user
    email = 'bob@bob.com'
    password = 'MyOldPwd'
    auth.register_user(email, password)

    # Generate reset password token
    try:
        reset_token = auth.get_reset_password_token(email)
        print(f"Reset Token: {reset_token}")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Update password using the reset token
    new_password = 'MyNewPwd'
    try:
        auth.update_password(reset_token, new_password)
        print("Password updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Verify login with the new password
    if auth.valid_login(email, new_password):
        print("Login successful with new password.")
    else:
        print("Login failed with new password.")


if __name__ == "__main__":
    main()
