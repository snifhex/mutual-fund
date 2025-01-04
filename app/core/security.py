from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

from app.auth.models import User
from app.core.config import get_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: User | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRY))
    to_encode = {"exp": expire, "sub": str(user.username), "id": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, get_settings().JWT_SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, get_settings().JWT_SECRET_KEY, algorithms=[get_settings().JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired") from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from err


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)
