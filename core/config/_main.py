import os
import secrets
from typing import List

from pydantic import EmailStr, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PREFIX: str = "/api/v1"
    SHOW_DOCS: bool = True
    PORT: int = 8000
    ORIGINS: List[str]

    BOT_WEBHOOK_URL: str
    BOT_WEB_APP_HOST: str
    BOT_TOKEN: str
    BOT_TEST_ENVIRONMENT: bool
    TEST_BOT_TOKEN: str

    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 120
    JWT_ALGORITHM: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn = None
    SQLALCHEMY_DEBUG: bool = False

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    COOKIE_SECURE: bool = False

    @field_validator("ORIGINS")
    @classmethod
    def set_default_origins(cls, v: List[str]) -> List[str]:
        defaults = ["http://localhost:3000", "http://127.0.0.1:3000"]
        return v + defaults

    class Config:
        env_file = os.path.abspath(".env")


AppConfig = _Config()
