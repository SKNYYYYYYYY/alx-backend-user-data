#!/usr/bin/python3
""" Check response
"""
import datetime
from time import sleep
import time
import os


if __name__ == "__main__":
    session_id = "a3277176-7663-4667-8c40-71d26cdb7361"
    with open('../del/del.txt', 'w') as f:
        f.write(f'curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=fe3d2f81-ce45-43b4-991d-e28ed153b1be"' )
    f.close()

curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=8c4186b4-9e97-41f2-8d30-d599bfa83b19"