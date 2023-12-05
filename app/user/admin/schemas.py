from datetime import datetime

from pydantic import BaseModel

from app.user.models import UserRole
from core.schemas.base import BaseORMSchema


class AdminUserBaseIDSchema(BaseModel):
    id: int


class AdminUserBase(BaseModel):
    email: str
    role: UserRole | None = None


class AdminUserBasePasswordSchema(BaseModel):
    password: str | None = None


class AdminUserBaseWithPassword(AdminUserBase, AdminUserBasePasswordSchema):
    pass


class AdminUserBaseSchema(BaseORMSchema, AdminUserBaseIDSchema, AdminUserBase):
    pass


class AdminLogInRequest(BaseModel):
    email: str
    password: str


class AdminLogInResponse(BaseModel):
    access_token: str
    refresh_token: str


class AdminAuthData(BaseModel):
    exp: datetime
    id: int
    email: str
    role: str
