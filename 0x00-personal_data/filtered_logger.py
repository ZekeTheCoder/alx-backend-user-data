#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in log messages.
"""

import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates the values of specified fields in a log message.
    """
    for field in fields:
        message = re.sub(
            rf'({field}=)([^;{separator}]*)', rf'\1{redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

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
