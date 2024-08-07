#!/usr/bin/env python3
""" Session Authentication Module """

import uuid
from api.v1.auth.auth import Auth


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
