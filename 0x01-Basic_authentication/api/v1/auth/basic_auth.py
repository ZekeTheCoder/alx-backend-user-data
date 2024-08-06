#!/usr/bin/env python3
""" Basic Authentication module """

import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication class inheriting from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract Base64 part from Authorization header."""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Strip off the "Basic " prefix (6 chars) and return remaining part
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode Base64 authorization header. """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes, validate=True)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract user credentials from Base64 decoded string"""

        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        # checks if the input contains the : character.
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the String and validate Split Length
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        if len(user_credentials) != 2:
            return None, None

        # email and password as a tuple
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Method that retrives User instance based on email & password"""

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Search for the user by email
            users = User.search({'email': user_email})

            # Ensure users is a list
            if not isinstance(users, list):
                return None

            # Check if the list is not empty and verify the password
            if users and users[0].is_valid_password(user_pwd):
                return users[0]

        except Exception:
            # If there's an exception (e.g., search fails), return None
            return None

        return None
