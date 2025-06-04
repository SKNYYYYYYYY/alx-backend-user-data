#!/usr/bin/env python3
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


my_db = DB()

# user_1 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# user_1 = my_db.add_user("test1@test.com", "AdvHashedPwd1")
# # print(user_1.id)

user_2 = my_db.add_user("test2@test.com", "BasicHashedPwd1")
# print(user_2.id)
try:
    my_db.update_user(user_2.id, hashed_password="tests@test.com")
    print(user_2.hashed_password)
except Exception as e:
    print("Error")