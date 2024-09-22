import jwt
from datetime import datetime, timedelta

# Secret key for encoding and decoding JWTs
SECRET_KEY = "your_secret_key"  # Change this to a strong secret
ALGORITHM = "HS256"

EXPIRATION_TIME = 2


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(hours=EXPIRATION_TIME)
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
