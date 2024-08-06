#!/usr/bin/env python3
""" Main 101
"""
from api.v1.auth.auth import Auth

a = Auth()

excluded_paths = ["/api/v1/stat*"]

print(a.require_auth("/api/v1/users", excluded_paths))   # True
print(a.require_auth("/api/v1/status", excluded_paths))  # False
print(a.require_auth("/api/v1/stats", excluded_paths))   # False

# python3 main_101.py to run
