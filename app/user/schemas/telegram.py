from pydantic import BaseModel


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
