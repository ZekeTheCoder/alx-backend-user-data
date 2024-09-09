#!/usr/bin/env python3
"""
This module provides a function to hash passwords using bcrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hashes a password using bcrypt with a salt. """
    salt = bcrypt.gensalt()
    encrypted = password.encode()
    hashed_password = bcrypt.hashpw(encrypted, salt)
    return hashed_password
