#!/usr/bin/env python3
"""
Session-based authentication module
"""


from .auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Class for session-based authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session for the given user ID

        Args:
            user_id (str, optional): User ID. Defaults to None.

        Returns:
            str: Session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user ID associated with the given session ID

        Args:
            session_id (str, optional): Session ID. Defaults to None.

        Returns:
            str: User ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Get the current user based on the session ID in the request

        Args:
            request (object, optional): Request object. Defaults to None.

        Returns:
            object: User object
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Destroy the session associated with the session ID in the request

        Args:
            request (object, optional): Request object. Defaults to None.

        Returns:
            bool: True if the session is destroyed, False otherwise
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
