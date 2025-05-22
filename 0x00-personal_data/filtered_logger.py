#!/usr/bin/env python3
"""
Module that contains filter_datum function to obfuscate specified fields in a log message.
"""
import re
from typing import List


def filter_datum(fields: List[str],redaction: str, message: str,separator: str) -> str:
    """Returns the log message with specified fields obfuscated using regex."""
    return re.sub(rf'({"|".join(fields)})=.*?{separator}',
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)
