#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)  # logs SQL
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return a User object."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the given filter criteria. """
        if not kwargs:
            raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the user with the given user_id using the provided keyword arguments."""
        valid_attributes = {'email', 'hashed_password',
                            'session_id', 'reset_token'}

        if not isinstance(user_id, int):
            raise ValueError("User ID must be an integer.")

        user = self.find_user_by(id=user_id)
        invalid_args = set(kwargs.keys()) - valid_attributes
        if invalid_args:
            raise ValueError(
                f"Invalid argument(s) provided: {', '.join(invalid_args)}")

        for key, value in kwargs.items():
            setattr(user, key, value)

        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise InvalidRequestError(
                f"An error occurred while updating the user: {e}") from e
