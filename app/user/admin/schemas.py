from pydantic import BaseModel

from app.user.models import UserRole
from app.user.schemas import UserCreate


#
class AdminUserCreateRequest(UserCreate):
    pass


class AdminUserUpdateRequest(BaseModel):
    telegram_id: int | None = None
    first_name: str | None = None
    role: UserRole | None = None
    email: str | None = None
    username: str | None = None
