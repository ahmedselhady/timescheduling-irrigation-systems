from sqlalchemy import Column, Integer, String, DateTime
from utils.database import base_db_entity

# Example: Define a User table model
class UserDB(base_db_entity):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # Fields for reset password functionality
    reset_token = Column(String, nullable=True)
    reset_token_expiration = Column(DateTime, nullable=True)
