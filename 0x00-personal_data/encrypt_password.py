#!/usr/bin/env python3
"""
This module provides a functions to hash passwords using bcrypt and
check if the provided password matches the hashed password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hashes a password using bcrypt with a salt. """
    salt = bcrypt.gensalt()
    encrypted = password.encode()
    hashed_password = bcrypt.hashpw(encrypted, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Checks if the provided password matches the hashed password. """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
