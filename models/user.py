from sqlalchemy import Column, Integer, String, Date
from utils.database import Base


# Example: Define a User table model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
