#!/usr/bin/env python3
"""
Auth class for managing user registration and authentication.
"""
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """ Hashes the given password using bcrypt and returns the salted,
                hashed password in bytes.
    """
    encrypted = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encrypted, salt)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if the email doesn't exist in the database."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)  # byte
# user = self._db.add_user(email, hashed_password.decode('utf-8')) # string
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate the login credentials and return boolean value """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create a session for the user with the given email and return the 
                                session ID or None If the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Finds user associated with the given session ID. """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session for the given user_id."""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
