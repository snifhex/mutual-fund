import base64
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/mutual_funds"
    JWT_SECRET_KEY: str = "JWT_SECRET_KEY"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRY: int = 86400
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    RAPIDAPI_KEY: str = "your-api-key"
    MF_RAPIDAPI_HOST: str = base64.b64decode("bGF0ZXN0LW11dHVhbC1mdW5kLW5hdi5wLnJhcGlkYXBpLmNvbQ==").decode("utf-8")
    MF_RAPIDAPI_BASE_URL: str = base64.b64decode(
        "aHR0cHM6Ly9sYXRlc3QtbXV0dWFsLWZ1bmQtbmF2LnAucmFwaWRhcGkuY29tCg=="
    ).decode("utf-8")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
