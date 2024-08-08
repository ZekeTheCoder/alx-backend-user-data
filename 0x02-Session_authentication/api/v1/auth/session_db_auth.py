#!/usr/bin/env python3
"""Module of Session authentication in a database"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication class that inherits from SessionExpAuth"""

    def create_session(self, user_id: str = None) -> str:
        """Create a new session ID with expiration and store it in the database
            Args:
                user_id: Identificator of the user_id
            Return:
                Session ID
        """

        session_id = super().create_session(user_id)

        if session_id is None:
            return None  # no session id found

        # Store session in the database
        user_session = UserSession(user_id=user_id, session_id=session_id)

        user_session.save()  # Save to the database
        # UserSession.save_to_file() #  to save multiple sessions

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get userID for sessionID from the database with expiration check
            Args:
                session_id: String of the session
            Return:
                User ID if not is expired
        """

        if session_id is None:
            return None  # no session id found

        # loads all session data from a file into memory
        UserSession.load_from_file()
        # search for a session that matches the given session_id
        user_session = UserSession.search({'session_id': session_id})

        if len(user_session) == 0:
            return None  # no sessions match the session_id

        user = user_session[0]  # first matching session

        if self.session_duration <= 0:
            return user.user_id  # if session not expired

        created_at = user.created_at

        if (created_at +
                timedelta(seconds=self.session_duration)) < datetime.utcnow():
            return None  # session is expired

        return user.user_id  # user_id associated with user session

    def destroy_session(self, request=None):
        """Destroy session by removing it from the database

        Return:
            True - session succesfuly destroyed, otherwise False
        """

        if request is None:
            return False  # no request is provided

        # Retrieve the session cookie from the request
        session_cookie = self.session_cookie(request)

        if not session_cookie:
            return False  # session cookie is not found

        # Search for the UserSession instance in the database
        user_session = UserSession.search({'session_id': session_cookie})

        if len(user_session) == 0:
            return False  # no matching session is found

        # Remove the session from the in-memory dictionary
        del self.user_id_by_session_id[session_cookie]
        # Remove the UserSession object from the database
        user_session[0].remove()

        return True  # session was successfully destroyed
