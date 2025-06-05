#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from db import DB

email = 'bob@bob.com'
password = 'mySuperPwd'
auth = Auth()
db = DB()


auth.register_user(email, password)
ses = (auth.create_session(email))

user = auth.get_user_from_session_id(session_id=ses)
tokn = user.reset_token

tokn = (auth.update_password(tokn, password="pwd"))

print((tokn))
# print(auth.create_session("unknown@email.com"))

