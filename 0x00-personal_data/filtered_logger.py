#!usr/bin/env python3
"""Filtering log messages"""
import re


def filter_datum(fields, redaction, message, separator):
	"""use regex to mask specified field's value"""
	pattern = r'(' + '|'.join(re.escape(field) for field in fields) + r')=([^;]+)'
	return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
