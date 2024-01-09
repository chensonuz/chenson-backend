from typing import Any, List

from pydantic import BaseModel

from app.user.models import UserRole
from app.user.utils import (
    get_random_password,
    get_random_phone_number,
)
from core.schemas.base import BaseORMSchema, BaseSchema, APIResponse


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


class UserID(BaseModel):
    id: int


class UserBase(BaseModel):
    telegram_id: int
    first_name: str
    role: UserRole | None = None
    email: str | None = None
    username: str | None = None
    photo_url: str | None = None


class UserBaseSchema(BaseORMSchema, UserID, UserBase, UserBasePasswordSchema):
    pass


class UserCreate(BaseSchema):
    role: UserRole = UserRole.Client
    telegram_id: int
    first_name: str
    phone_number: str = get_random_phone_number()
    password: str = get_random_password()
    username: str | None = None
    photo_url: str | None = None


class UserResponse(BaseORMSchema, UserID, UserBase):
    pass


class UserShortResponse(BaseORMSchema, UserID):
    first_name: str
    telegram_id: int
    phone_number: str | None = None

    def mention_html(self) -> str:
        """Mention the user in the best way possible given the available data."""
        return (
            f"<a href='tg://user?id={self.telegram_id}'>{self.first_name}</a>"
        )


class UserSignInUpResponse(BaseModel):
    created: bool
    user: UserResponse


class RequestSMSRequest(BaseModel):
    phone_number: str


class APIUserResponse(APIResponse):
    data: UserResponse | None = None


class APIUserListResponse(APIResponse):
    data: List[UserResponse] = None


class APIRequestSMSResponse(APIResponse):
    data: Any = None


class APISignInUpResponse(APIResponse):
    data: UserSignInUpResponse | None = None
