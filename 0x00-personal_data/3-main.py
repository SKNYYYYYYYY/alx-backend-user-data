#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()
cur = db.cursor()
cur.execute("SELECT COUNT(*) FROM pii_users;")
for row in cur:
	print(row[0])
cur.close()
db.close()

