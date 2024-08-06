#!/usr/bin/env python3
""" Module that manages the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ This class is the template for all authentication system """

    def __init__(self):
        """Initialize the Auth class."""
        pass  # Currently no initialization needed

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path."""
        return False  # Path and excluded_paths will be used later

    def authorization_header(self, request=None) -> str:
        """Return the authorization header from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user from the request."""
        return None
