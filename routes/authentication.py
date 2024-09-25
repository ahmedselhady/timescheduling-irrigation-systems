from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, timedelta

from utils.database import get_db_session, base_db_entity
from utils.mailing import send_email
from models.user import UserDB
from utils.hashing import hash_password, verify_password
from utils.token_generator import create_access_token
import secrets

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
def signup(user: User, db: Session = Depends(get_db_session)):
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
def login(login_data: LoginRequest, db: Session = Depends(get_db_session)):
    # Retrieve user from database
    user = db.query(UserDB).filter(UserDB.email == login_data.email).first()
    # if not user or password != user.password:
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create a token
    access_token = create_access_token(data={"sub": user.email})

    return {"message": "Login successful!", "access_token": access_token}


# Pydantic model for reset password request
class ResetPasswordRequest(BaseModel):
    email: EmailStr


# Reset password endpoint
@router.post("/reset")
def reset_password(
    request: ResetPasswordRequest, db: Session = Depends(get_db_session)
):
    # Find user by email
    user = db.query(UserDB).filter(UserDB.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate a random reset token and set expiration time
    reset_token = secrets.token_hex(
        16
    )  # Generates a 16-byte token, represented as 32-character hexadecimal
    reset_token_expiration = datetime.utcnow() + timedelta(hours=2)

    # Update the user with the reset token and expiration time
    user.reset_token = reset_token
    user.reset_token_expiration = reset_token_expiration
    db.commit()

    # Send an email to the user with the reset token
    reset_link = f"http://example.com/reset-password?token={reset_token}"  # Waiting the frontend's reset link
    send_email(
        to=user.email,
        subject="Typical's account password reset request",
        body=f"Please use the following link to reset your password: {reset_link}.\nThis link is valid for 2 hours.",
    )

    return {"message": "Password reset email has been sent successfully!"}


# Pydantic model for the reset password request
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str

    @validator("new_password")
    def password_must_be_at_least_8_chars(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


@router.post("/new-password")
def reset_password(
    reset_data: ResetPasswordRequest, db: Session = Depends(get_db_session)
):
    # Find the user by email
    user = db.query(UserDB).filter(UserDB.email == reset_data.email).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="User with this email does not exist"
        )

    # Validate the reset token
    if user.reset_token != reset_data.reset_token:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    
    # Check if the token doesn't exist
    if not user.reset_token_expiration:
        raise HTTPException(status_code=400, detail="There is no reset token")
    
    # Check if the token has expired
    if user.reset_token_expiration and user.reset_token_expiration < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired")

    # Update the user's password
    user.password = hash_password(reset_data.new_password)

    # Nullify the reset token and its expiration
    user.reset_token = None
    user.reset_token_expiration = None

    # Save the changes
    db.commit()

    return {"message": "Password reset successfully"}
