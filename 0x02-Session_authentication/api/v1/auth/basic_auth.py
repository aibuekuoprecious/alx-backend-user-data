#!/usr/bin/env python3
"""
Basic authentication Module
"""


from typing import TypeVar
from api.v1.auth.auth import Auth
import base64

from models.user import User


class BasicAuth(Auth):
    """
    Class for Basic authentication
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """
        Extracts the base64 authorization header from the given header string

        Args:
            auth_header (str): The authorization header string

        Returns:
            str: The base64 authorization header
        """
        if auth_header is None:
            return None
        if not isinstance(auth_header, str):
            return None
        if not auth_header.startswith("Basic "):
            return None

        token = auth_header.split(" ")[-1]
        return token

    def decode_base64_authorization_header(self, base64_header: str) -> str:
        """
        Decodes the base64 authorization header

        Args:
            base64_header (str): The base64 authorization header

        Returns:
            str: The decoded authorization header
        """
        if base64_header is None:
            return None
        if not isinstance(base64_header, str):
            return None

        try:
            item_to_decode = base64_header.encode("utf-8")
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_header: str) -> (str, str):
        """
        Extracts the user credentials from the decoded authorization header

        Args:
            decoded_header (str): The decoded authorization header

        Returns:
            tuple: A tuple containing the email and password
        """
        if decoded_header is None:
            return (None, None)
        if not isinstance(decoded_header, str):
            return (None, None)
        if ":" not in decoded_header:
            return (None, None)

        email, password = decoded_header.split(":")
        return (email, password)

    def user_object_from_credentials(
        self, email: str, password: str
    ) -> TypeVar("User"):
        """
        Retrieves the user object based on the given email and password

        Args:
            email (str): The user's email
            password (str): The user's password

        Returns:
            User: The user object if found, None otherwise
        """
        if email is None or not isinstance(email, str):
            return None
        if password is None or not isinstance(password, str):
            return None

        try:
            users = User.search({"email": email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(password):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves the current user based on the request's authorization header

        Args:
            request (optional): The request object

        Returns:
            User: The current user object if found, None otherwise
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, password)

        return None
