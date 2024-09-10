#!/usr/bin/env python3
"""
This module contains authentication functions.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashes the given password using bcrypt and returns the salted,
                hashed password in bytes.
    """
    salt = bcrypt.gensalt()
    encrypted = password.encode('utf-8')
    return bcrypt.hashpw(encrypted, salt)
