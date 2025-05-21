#!/usr/bin/env python3
"""filters PII in a log message"""
import re


def filter_datum(fields, redaction, message, separator):
	"""obfuscate strings in fields"""
	pattern = r'(' + '|'.join(re.escape(field) for field in fields) + r')=([^;]+)'
	return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
