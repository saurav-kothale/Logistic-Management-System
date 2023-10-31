from sqlalchemy import Column, String

from database.db import base


class User(base):
    __tablename__ = "user"
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, primary_key=True)
    user_id = Column(String , unique = True)
    email_id = Column(String, unique=True)
    mobile_no = Column(String, unique=True)
    password = Column(String)
    retype_password = Column(String)
