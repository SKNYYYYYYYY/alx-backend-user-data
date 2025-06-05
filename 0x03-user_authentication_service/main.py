#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from db import DB

email = 'bob@bodsjhb.com'
password = 'MyPwdOfsdBob'
auth = Auth()
db = DB()


auth.register_user(email, password)
ses = (auth.create_session(email))
# user = auth.get_user_from_session_id(session_id=ses)
# print(auth.destroy_session(user_id=user.id))
# print(auth.get_user_from_session_id(session_id=ses))
# print(auth.create_session("unknown@email.com"))

