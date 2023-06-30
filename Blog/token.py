from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas

SECRET_KEY = "27f5e472154a507f19c770743fb0aae3c2f776e2e65d7e1c31f7c5846b92165d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 15


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenDate(email=email)
    except JWTError:
        raise credentials_exception
