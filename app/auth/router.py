from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.auth.models import User
from app.auth.schemas import CreateUserRequest, Token, UserResponse
from app.auth.service import authenticate_user
from app.core.database.deps import db_dependency
from app.core.security import create_access_token, get_password_hash

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user: CreateUserRequest) -> UserResponse:
    create_user_model = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(create_user_model)
    db.commit()
    return UserResponse(
        id=str(create_user_model.id),
        username=create_user_model.username,
        created_at=create_user_model.created_at,
        updated_at=create_user_model.updated_at,
    )


@auth_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = create_access_token(user, timedelta(minutes=15))
    return {"access_token": access_token, "token_type": "bearer"}
