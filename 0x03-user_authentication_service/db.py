#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the users.

        Returns:
            User: The first user found.

        Raises:
            InvalidRequestError: If no keyword arguments are provided.
            NoResultFound: If no user is found.
            MultipleResultsFound: If multiple users are found.
        """
        if not kwargs:
            raise InvalidRequestError("No keyword arguments provided.")

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound("No user found.")
            return user
        except MultipleResultsFound:
            raise NoResultFound("Multiple users found.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the user attributes to update.

        Raises:
            ValueError: If an invalid attribute is passed.

        Returns:
            None
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
        return None
