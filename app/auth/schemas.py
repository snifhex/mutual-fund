from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str = Field(..., description="The access token")
    token_type: str = Field(..., description="The type of the token")

    model_config = ConfigDict(json_schema_extra={"example": {"access_token": "ACCESS_TOKEN", "token_type": "bearer"}})


class CreateUserRequest(BaseModel):
    username: str = Field(..., description="The username/email of the user")
    password: str = Field(..., description="The password of the user")

    model_config = ConfigDict(json_schema_extra={"example": {"username": "john_doe@email.com", "password": "password"}})


class UserResponse(BaseModel):
    id: str = Field(..., description="The id of the user")
    username: str = Field(..., description="The username of the user")
    created_at: datetime = Field(..., description="The creation date of the user")
    updated_at: datetime = Field(..., description="The last update date of the user")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "1",
                "username": "john_doe@email.com",
                "created_at": "2021-01-01",
                "updated_at": "2021-01-01",
            }
        }
    )
