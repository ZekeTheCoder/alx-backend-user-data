#!/usr/bin/env python3
"""
Auth class for managing user registration and authentication.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hashes the given password using bcrypt and returns the salted,
                hashed password in bytes.
    """
    salt = bcrypt.gensalt()
    encrypted = password.encode('utf-8')
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
