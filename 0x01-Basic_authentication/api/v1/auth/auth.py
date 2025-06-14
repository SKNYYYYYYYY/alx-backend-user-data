#!/usr/bin/env python3
"""
Authentication module
"""
from typing import List, TypeVar


class Auth():
    """class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return False"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/') + '/'
        for expath in excluded_paths:
            if expath.endswith("*"):
                if (path.startswith(expath[:-1])):
                    return False
            else:
                expath = expath.rstrip('/') + '/'
                if path == expath:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """return None"""
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """return None"""
        return None
