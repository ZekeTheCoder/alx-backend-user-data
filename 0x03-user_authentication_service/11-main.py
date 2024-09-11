#!/usr/bin/env python3
"""
Main file to test the /profile route.
"""

import requests

BASE_URL = "http://localhost:5000"


def test_profile_route():
    """Test the /profile route."""

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

    # Extract the session_id from cookies
    session_id = response.cookies.get('session_id')
    if not session_id:
        print("Failed to get session_id cookie")
        return

    # Now request the profile
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={'session_id': session_id},
                            timeout=60)
    print("Profile Response:", response.json())

    # Test with an invalid session_id
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={'session_id': 'invalid_session_id'},
                            timeout=60)
    print("Invalid Session Response:", response.json())


if __name__ == "__main__":
    test_profile_route()
