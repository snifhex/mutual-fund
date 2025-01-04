from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette import status

from app.auth.models import User
from app.core.database.deps import db_dependency
from app.core.security import verify_access_token, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_user(username: str, password: str, db: db_dependency) -> User | bool:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    try:
        payload = verify_access_token(token)
        username: str = payload.get("sub")
        id: str = payload.get("id")
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {"username": username, "id": id}
    except PyJWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user") from err
