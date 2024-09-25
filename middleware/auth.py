from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import yaml

# Secret key for encoding and decoding JWTs
# Load configuration from YAML file
with open("./utils/secrets.yaml", "r") as file:
    config = yaml.safe_load(file)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Function to verify token
def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            config["security"]["SECRET_KEY"],
            algorithms=[config["security"]["ALGORITHM"]],
        )
        # Extract email or other identity from the token
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email
