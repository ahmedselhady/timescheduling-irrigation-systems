import jwt
import yaml
from datetime import datetime, timedelta

# Secret key for encoding and decoding JWTs
with open("./utils/secrets.yaml", "r") as file:
    config = yaml.safe_load(file)


EXPIRATION_TIME = 2


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(hours=EXPIRATION_TIME)
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        config["security"]["SECRET_KEY"],
        algorithm=config["security"]["ALGORITHM"],
    )
