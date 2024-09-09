#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in log messages.
"""

import re
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
