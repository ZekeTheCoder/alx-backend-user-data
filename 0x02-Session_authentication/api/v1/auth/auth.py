#!/usr/bin/env python3
""" Module that manages the API authentication.
"""
from os import getenv
from typing import List, TypeVar
from flask import request


class Auth:
    """ This class is the template for all authentication system """

    def __init__(self):
        """Initialize the Auth class."""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path.
            Args:
                path: path to authenticate
                excluded_paths: list of excluded path to authenticate
            Return:
                True if is authenticated otherwise false
        """
        # Check if path is None, excluded_paths is None, or is empty
        if path is None or not excluded_paths:
            return True

        # Ensure path ends with a '/'
        if path[-1] != '/':
            path += '/'

        # Check if path matches any pattern in excluded_paths
        for excluded_path in excluded_paths:
            # Check path starts with the excluded_path prefix (excluding '*')
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            # Check for an exact match with an excluded path
            elif path == excluded_path:
                return False

        # If no exclusions match, authentication is required
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the value of the Authorization header from the request.
        Args:
            request: The request object.
        Returns:
            The value of the Authorization header if it exists, otherwise None.
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user from the request.
        Args:
            request: The request object.
        Returns:
            None
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Extracts the session cookie value from the request.
        Args:
            request (flask.Request): The request object containing cookies.
        Returns:
            str: The value of the session cookie if it exists, otherwise None.
        """
        if request is None:
            return None

        cookie_name = getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(cookie_name)
