#!/usr/bin/env python3
""" Module of Session Auth Expiration."""

from typing import Dict
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication class."""

    def __init__(self):
        """ Initialize with session duration from environment variable.
        """
        # Get SESSION_DURATION from environment variable;
        session_duration = getenv('SESSION_DURATION', 0)  # default to 0

        try:
            # Convert SESSION_DURATION to integer
            self.session_duration = int(session_duration)
        except ValueError:
            # Handle conversion errors by setting session_duration to 0
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session ID with expiration.
        Args:
            user_id (str): Identifier of the user.
        Returns:
            str: Session ID if created successfully, otherwise None.
        """
        # Call the create_session method from the parent class
        session_id = super().create_session(user_id)

        if session_id is None:
            # Return None if session creation fails
            return None

        # Create session dictionary with expiration
        session_dictionary: Dict = {
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }

        # Store the session dictionary in the class attribute
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user ID for session ID with expiration check.
        Args:
            session_id (str): Session ID to check.
        Returns:
            str: User ID if the session is valid and not expired, else None.
        """
        if session_id is None:
            return None  # Return None if session_id is not provided

        # Retrieve the session dictionary for the given session_id
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None  # Return None if session ID does not exist

        if self.session_duration <= 0:
            # If session_duration is 0 or negative, sessions do not expire
            return session_dictionary.get('user_id')

        # Get the creation time of the session
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None  # Return None if creation time is not available

        # Calculate expiration time
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        # Check if the session has expired
        if datetime.utcnow() > expiration_time:
            # Remove expired session
            del self.user_id_by_session_id[session_id]
            return None

        return session_dictionary.get('user_id')
