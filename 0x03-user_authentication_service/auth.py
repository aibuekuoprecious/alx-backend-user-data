#!/usr/bin/env python3
"""Auth class to interact with the authentication database."""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.hashpw.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a new UUID and returns it as a string.

    Returns:
        str: The string representation of the generated UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """Registers a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            Union[None, User]: The registered user object or None if registration fails.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            # Add user to database
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            Boolean: _description_
        """
        try:
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # check validity of password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user_session_id(user.id, session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user corresponding to the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The corresponding user or None if not found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by_session_id(session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the user with the given user ID.

        Args:
            user_id (int): The ID of the user.
        """
        user = self._db.find_user_by_id(user_id)
        if user:
            self._db.update_user_session_id(user.id, None)

    def get_reset_password_token(self, email: str) -> str:
        """Get the reset password token for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password using the reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        user.hashed_password = _hash_password(password)
        user.reset_token = None
