from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from datetime import date

from utils.database import get_db, Base
from models.user import UserDB
from utils.hashing import hash_password, verify_password
from utils.token_generator import create_access_token

router = APIRouter()


# Define a Pydantic model for sign up request
class User(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @validator("password")
    def password_must_be_at_least_8_chars(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


# sign-up route
@router.post("/signup")
def signup(user: User, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create a new user with hashed password
    new_user = UserDB(
        email=user.email,
        # password=user.password,
        password=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User signed up successfully!"}


# Define a Pydantic model for login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Login route
@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Retrieve user from database
    user = db.query(UserDB).filter(UserDB.email == login_data.email).first()
    # if not user or password != user.password:
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create a token
    access_token = create_access_token(data={"sub": user.email})

    return {"message": "Login successful!", "access_token": access_token}
