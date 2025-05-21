#!/usr/bin/env python3
"""
Main file
"""
filter_datum = __import__('filtered_logger').filter_datum
fields = ['password', "date_of_birth"]
messages = ["name=egg;email=egg@example.com;password=eggpwd;date_of_birth=12/12/2004;", "name=bob;email=bob@example.com;password=bobpwd;date_of_birth=06/12/1992;"]

for message in messages:
	print(filter_datum(fields, 'xxx', message, ';'))