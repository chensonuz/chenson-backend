import enum

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class UserRole(enum.Enum):
    Admin = "Admin"
    Client = "User"


class User(Base, CreatedUpdatedMixin):
    __tablename__ = "users"

    role: Mapped[UserRole]
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    email: Mapped[str | None]
    password: Mapped[str]
    username: Mapped[str | None]
    phone_number: Mapped[str | None]
    photo_url: Mapped[str | None]
