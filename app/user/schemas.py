from pydantic import BaseModel

from app.user.models import UserRole
from app.user.utils import (
    get_random_password,
    get_random_phone_number,
)
from core.schemas.base import BaseORMSchema, BaseSchema


class Chat(BaseModel):
    id: int
    type: str
    title: str
    username: str | None = None
    photo_url: str | None = None


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    added_to_attachment_menu: bool | None = False
    allows_write_to_pm: bool | None = False
    is_premium: bool | None = False
    photo_url: str | None = None


class InitData(BaseModel):
    query_id: str
    user: TelegramUser
    auth_date: int
    hash: str
    chat: Chat | None = None
    receiver: TelegramUser | None = None
    chat_type: str | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None


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
