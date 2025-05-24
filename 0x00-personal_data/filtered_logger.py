#!/usr/bin/env python3
"""
Contains filter_datum function to obfuscate specified fields in a log message.
"""
import re
from typing import List, cast
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message with specified fields obfuscated using regex."""
    return re.sub(rf'({"|".join(fields)})=.*?{separator}',
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """custom formater"""
    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s: %(message)s"
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]) -> None:
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


# PII_FIELDS = ("email", "name", "ssn", "password", "phone",)


# def get_logger() -> logging.Logger:
#     """get logger"""
#     logger = logging.getLogger("user_data")
#     logger.setLevel(logging.INFO)
#     logger.propagate = False
#     console = logging.StreamHandler()
#     formatter = RedactingFormatter(fields=list(PII_FIELDS))
#     console.setFormatter(formatter)
#     logger.addHandler(console)
#     return logger


# def get_db() -> MySQLConnection:
#     """return db connector"""
#     username = os.getenv("PERSONAL_DATA_DB_USERNAME", default="root")
#     host = os.getenv("PERSONAL_DATA_DB_HOST", default="localhost")
#     password = os.getenv("PERSONAL_DATA_DB_PASSWORD", default="")
#     db_name = os.getenv("PERSONAL_DATA_DB_NAME")
#     conn = mysql.connector.connect(
#         host=host,
#         user=username,
#         password=password,
#         database=db_name
#     )
#     return cast(MySQLConnection, conn)


# def main() -> None:
#     """returns nothing"""
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM pii_users")
#     rows = cur.fetchall()
#     logger = get_logger()
#     for name, email, phone, ssn, password, ip, last_login, user_agent in rows:
#         logger.info(f"name={name}; email={email}; phone={phone}; ssn={ssn}; password={
#                     password}; ip={ip};last_login={last_login}; user_agent={user_agent};")


# if __name__ == '__main__':
#     main()
