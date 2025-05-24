#!/usr/bin/env python3
"""
Contains filter_datum function to obfuscate specified fields in a log message.
"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message with specified fields obfuscated using regex."""
    return re.sub(rf'({"|".join(fields)})=.*?{separator}',
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """custom formater"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(levelname)s %(asctime)s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor"""
        self.fields = fields
        super().__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """redact pii"""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("email", "phone", "ssn", "password", "ip",)


def get_logger() -> logging.Logger:
    """get logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    console = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger
