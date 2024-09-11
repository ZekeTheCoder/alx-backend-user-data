#!/usr/bin/env python3
"""
13-Main file - 17. Get reset password token.
"""
import requests

BASE_URL = "http://localhost:5000"


def test_reset_password(email: str):
    """Test the reset password functionality."""
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})

    if response.status_code == 200:
        print(f"Success: {response.json()}")
    elif response.status_code == 403:
        print("Error: Email not registered.")
    else:
        print(f"Unexpected status code: {response.status_code}")


if __name__ == "__main__":
    test_reset_password("bob@bob.com")  # valid email
    test_reset_password("unknown@example.com")  # invalid email
    test_reset_password("")  # empty email
