#!/usr/bin/env python3
"""
1-Main file
"""

import logging
from db import DB
from user import User

# Suppress SQLAlchemy logging
# logging.basicConfig(level=logging.ERROR)
# logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
# logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
logging.disable(logging.CRITICAL)

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)
