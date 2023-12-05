from datetime import datetime, timedelta
from typing import List

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger

from app.admin.schemas import AdminAuthData
from app.user.models import UserRole
from core.config import AppConfig
from core.exceptions.classes import ForbiddenError, UnauthorizedError


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                logger.warning("Invalid authentication scheme.")
                raise ForbiddenError("Invalid authentication scheme.")
            verify_access_token(credentials.credentials)
            return credentials.credentials
        else:
            logger.warning("Invalid authorization code.")
            raise ForbiddenError("Invalid authorization code.")


def create_access_token(subject: dict, expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=AppConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    data = {
        "exp": expires_delta,
        "id": int(subject["id"]),
        "email": str(subject["email"]),
        "role": str(subject["role"]),
    }
    encoded_jwt = jwt.encode(
        data, AppConfig.ACCESS_SECRET_KEY, AppConfig.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(subject: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=AppConfig.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    data = {
        "exp": expires_delta,
        "id": int(subject["id"]),
        "email": str(subject["email"]),
        "role": str(subject["role"]),
    }
    encoded_jwt = jwt.encode(
        data, AppConfig.REFRESH_SECRET_KEY, AppConfig.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> None:
    try:
        jwt.decode(
            token,
            AppConfig.ACCESS_SECRET_KEY,
            algorithms=[AppConfig.JWT_ALGORITHM],
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise UnauthorizedError("Access token expired.")
    except jwt.exceptions.InvalidSignatureError:
        raise ForbiddenError("Invalid access token.")
    except jwt.exceptions.DecodeError:
        raise ForbiddenError("Invalid access token.")


def verify_refresh_token(token: str) -> None:
    try:
        jwt.decode(
            token,
            AppConfig.REFRESH_SECRET_KEY,
            algorithms=[AppConfig.JWT_ALGORITHM],
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise UnauthorizedError("Refresh token expired.")
    except jwt.exceptions.InvalidSignatureError:
        raise ForbiddenError("Invalid refresh token.")
    except jwt.exceptions.DecodeError:
        raise ForbiddenError("Invalid refresh token.")


async def get_current_admin(token: str = Depends(JWTBearer())) -> AdminAuthData:
    payload = jwt.decode(
        token, AppConfig.ACCESS_SECRET_KEY, algorithms=[AppConfig.JWT_ALGORITHM]
    )
    if payload is None:
        logger.warning("Credentials are not valid!")
        raise UnauthorizedError("Credentials are not valid!")
    admin_user_id: int = payload.get("id")
    if admin_user_id is None:
        logger.warning("Credentials are not valid!")
        raise UnauthorizedError("Credentials are not valid!")
    return AdminAuthData.model_validate(payload)


class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = [role.value.casefold() for role in allowed_roles]

    def __call__(self, user: AdminAuthData = Depends(get_current_admin)):
        if user.role.casefold() not in self.allowed_roles:
            raise ForbiddenError("Access denied.")
