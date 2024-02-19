#!/usr/bin/env python3
"""
Module for authentication using Basic auth
"""


from typing import TypeVar
from api.v1.auth.auth import Auth
import base64

from models.user import User


class BasicAuth(Auth):
    """
    Class for Basic authentication.

    This class provides methods for extracting and decoding the base64 authorization header,
    extracting user credentials, and retrieving the current user based on the provided credentials.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the base64 authorization header from the given authorization header.

        Args:
            authorization_header (str): The authorization header.

        Returns:
            str: The base64 authorization header.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes the base64 authorization header.

        Args:
            base64_authorization_header (str): The base64 authorization header.

        Returns:
            str: The decoded authorization header.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None

        try:
            item_to_decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user credentials from the decoded base64 authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded base64 authorization header.

        Returns:
            tuple: A tuple containing the email and password extracted from the authorization header.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the user object based on the provided email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The user object if the email and password are valid, None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the provided request.

        Args:
            request (optional): The request object.

        Returns:
            User: The current user object if the request contains a valid authorization header,
            None otherwise.
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
