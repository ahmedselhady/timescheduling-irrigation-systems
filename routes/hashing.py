from passlib.context import CryptContext

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)


# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
