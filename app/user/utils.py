import random
import string

from fastapi import Response
from passlib.context import CryptContext

from core.config import AppConfig

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_random_password() -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"

    return hash_password(
        password="".join([random.choice(chars) for i in range(13)])
    )


def get_random_phone_number() -> str:
    return "+998" + "".join([random.choice(string.digits) for i in range(9)])


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def response_set_secure_cookie(
    response: Response, key: str, token: str, time: int
):
    return response.set_cookie(
        key=key,
        value=token,
        max_age=time,
        expires=time,
        path="/",
        domain=None,
        secure=AppConfig.COOKIE_SECURE,
        httponly=True,
        samesite="none",
    )


def delete_token(response: Response, key: str):
    return response.delete_cookie(
        key=key,
        path="/",
        domain=None,
        secure=AppConfig.COOKIE_SECURE,
        httponly=True,
        samesite="none",
    )
