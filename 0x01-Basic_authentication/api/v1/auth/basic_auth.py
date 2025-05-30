#!/usr/bin/env python3
"""basic auth module"""
import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """handles basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.strip('Basic ')

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decodes base64 Authorization header"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ returns the User instance"""
        if user_email is None:
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        User.load_from_file()
        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request using Basic Auth."""
        # Step 1: Get the Authorization header from the request
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        # Step 2: Extract base64 part
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if not base64_auth:
            return None
        # Step 3: Decode the base64 string
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if not decoded_auth:
            return None
            # Step 4: Extract user email and password
        credentials = self.extract_user_credentials(decoded_auth)
        if not credentials or len(credentials) != 2:
            return None
        user_email, user_pwd = credentials
        # Step 5: Retrieve the User instance
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
