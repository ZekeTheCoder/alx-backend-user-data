#!/usr/bin/env python3
"""
15-Main file - 19. Update password end-point
"""
import requests

BASE_URL = "http://localhost:5000"


def test_reset_password_route():
    """Test the /reset_password route (password update functionality)."""

    # First, register a new user
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    response = requests.post(
        f"{BASE_URL}/users", data={'email': email, 'password': password},
        timeout=60)
    print("Register User Response:", response.json())

    # Log in to create a session
    response = requests.post(f"{BASE_URL}/sessions",
                             data={'email': email, 'password': password},
                             timeout=60)
    print("Login Response:", response.json())

    # Request a reset password token
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={'email': email},
                             timeout=60)
    print("Reset Password Token Response:", response.json())

    # Extract the reset token from the response
    reset_token = response.json().get('reset_token')
    if not reset_token:
        print("Failed to get reset token")
        return

    # Use the reset token to update the password
    new_password = 'NewPassword123'
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={'email': email, 'reset_token': reset_token,
                                  'new_password': new_password},
                            timeout=60)
    print("Password Update Response:", response.json())

    # Now log in with the new password
    response = requests.post(f"{BASE_URL}/sessions",
                             data={'email': email, 'password': new_password},
                             timeout=60)
    print("Login with New Password Response:", response.json())

    # Test with an invalid reset token
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={'email': email, 'reset_token': 'invalid_reset_token',
                                  'new_password': new_password},
                            timeout=60)

    # Check if the response is in JSON format
    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError:
        json_response = {"error": "Non-JSON response",
                         "status_code": response.status_code}

    print("Invalid Reset Token Response:", json_response)


if __name__ == "__main__":
    test_reset_password_route()
