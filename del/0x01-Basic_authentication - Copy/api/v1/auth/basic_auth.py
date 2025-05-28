#!/usr/bin/env python3
"""basic auth module"""
import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import is_valid_password, User


class BasicAuth(Auth):
	"""handles basic authentication"""
	def extract_base64_authorization_header(self, authorization_header: str) -> str:
		"""returns the Base64 part of the Authorization header"""
		if authorization_header is None or not isinstance(authorization_header, str):
			return None
		if not authorization_header.startswith('Basic '):
			return None
		else:
			return authorization_header.strip('Basic ')

	def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
		"""decodes base64 Authorization header"""
		if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
			return None
		try:
			decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
			return decoded_bytes.decode()
		except  binascii.Error:
			return None

	def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
		"""returns the user email and password"""
		if decoded_base64_authorization_header  is None or not isinstance(decoded_base64_authorization_header , str):
			return None, None
		
		if ':' not in decoded_base64_authorization_header:
			return None, None
		email, password = decoded_base64_authorization_header.split(':')
		return email, password

	def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
		""" returns the User instance"""
		if user_email is None:
			return None
		if user_pwd is None or not isinstance(user_pwd, str):
			return None

		user = User.find_by_email(user_email)
		if user is None:
			return None
		if not user.is_valid_password(user_pwd):
			return None
		return user