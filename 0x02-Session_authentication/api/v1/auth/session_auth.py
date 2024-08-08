#!/usr/bin/env python3
""" Session-based Authentication Module """

import uuid
from os import getenv
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session Authentication class inheriting from Auth. """

    # empty dictionary to store session IDs and their associated user IDs.
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID for a user_id
        Args:
            user_id (str): The user ID to create a session for
        Returns:
            str: The new session ID if successful, None otherwise
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary with user_id as value
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve the User ID associated with a Session ID.
        Args:
            session_id (str): The session ID to look up.
        Returns:
            str: The associated User ID if session ID is valid, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieve a User instance based on the session cookie value.
        Args:
            request: The request object to extract the session cookie from.
        Returns:
            User: User instance associated with the session ID if found,
            otherwise None
        """
        # Get the session ID from the request's cookies
        session_id = self.session_cookie(request)

        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Fetch and return the User instance from the database
        return User.get(user_id)

    def session_cookie(self, request=None):
        """Retrieve the session cookie value from the request.
        Args:
            request: The request object to extract the cookie from.
        Returns:
            str: value of the session cookie if it exists, otherwise None.
        """
        if request is None:
            return None

        # Get the cookie value from SESSION_NAME environment variable
        cookie_name = getenv('SESSION_NAME')
        if not cookie_name:
            return None

        return request.cookies.get(cookie_name)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logs out the user.
        Args:
            request: The incoming request object. Defaults to None.
        Returns:
            bool: True if the session successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        # Retrieve session ID from the request cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Remove session ID from the dictionary
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
