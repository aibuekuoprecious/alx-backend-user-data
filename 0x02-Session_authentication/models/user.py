#!/usr/bin/env python3
""" User module
"""
import hashlib
from models.base import Base


class User(Base):
    """Represents a user in the system.

    Attributes:
        email (str): The email address of the user.
        password (str): The encrypted password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Getter for the password.

        Returns:
            str: The encrypted password.
        """
        return self._password

    @password.setter
    def password(self, new_password: str):
        """Setter for a new password: encrypt in SHA256.

        Args:
            new_password (str): The new password to be set.
        """
        if new_password is None or type(new_password) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(
                new_password.encode()).hexdigest().lower()

    def is_valid_password(self, password: str) -> bool:
        """Validate a password.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if password is None or type(password) is not str:
            return False
        if self.password is None:
            return False
        password_encoded = password.encode()
        return hashlib.sha256(password_encoded).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Display User name based on email/first_name/last_name.

        Returns:
            str: The display name of the user.
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
