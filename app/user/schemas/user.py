from pydantic import BaseModel

from app.user.database.models import UserRole
from app.user.utils import (
    get_random_password,
    get_random_phone_number,
)
from core.schemas.base import BaseORMSchema, BaseSchema


class UserBasePasswordSchema(BaseModel):
    password: str | None = None


class UserBaseIDSchema(BaseModel):
    id: int


class UserBase(BaseModel):
    telegram_id: int
    first_name: str
    role: UserRole | None = None
    email: str | None = None
    username: str | None = None


class UserBaseSchema(
    BaseORMSchema, UserBaseIDSchema, UserBase, UserBasePasswordSchema
):
    pass


class UserCreate(BaseSchema):
    role: UserRole = UserRole.Client
    telegram_id: int
    first_name: str
    phone_number: str = get_random_phone_number()
    password: str = get_random_password()
    username: str | None = None


class UserResponse(BaseORMSchema, UserBaseIDSchema, UserBase):
    pass
