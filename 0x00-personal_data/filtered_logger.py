#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in log messages.
"""

import re
import logging
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the formatter with the fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters the log record's message to redact specified fields."""
        original_msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_msg,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates the values of specified fields in a log message.
    """
    for field in fields:
        message = re.sub(
            rf'({field}=)([^;{separator}]*)', rf'\1{redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger with PII data filtering.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to MySQL database using credentials from environment variables.
    """
    return mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME', 'root'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''))


def main():
    """Obtain a database connection using get_db, retrieves all rows
                from the users table and logs each row with filtered data."""
    logger = get_logger()
    db_connection = get_db()
    cursor = db_connection.cursor(dictionary=True)

    query = "SELECT * FROM users;"
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        log_message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(log_message)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
