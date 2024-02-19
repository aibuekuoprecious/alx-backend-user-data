#!/usr/bin/env python3
"""
Module for authentication
"""


from typing import Dict, TypeVar
from flask import request


class Auth:
    """Class for authentication"""

    def __init__(self):
        self.excluded_paths: Dict[str, bool] = {}

    def require_auth(self, path: str) -> bool:
        """Check if authentication is required for a given path"""
        if path is None:
            return True

        if not self.excluded_paths:
            return True

        for excluded_path in self.excluded_paths:
            if excluded_path == path or path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, req=None) -> str:
        """Get the authorization header from the request"""
        if req is None:
            return None

        header = req.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, req=None) -> TypeVar('User'):
        """Get the current user"""
        return None
