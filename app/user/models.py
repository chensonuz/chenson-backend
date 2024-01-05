import enum

from sqlalchemy import BigInteger, ForeignKey
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


class AddressInfo(Base, CreatedUpdatedMixin):
    __tablename__ = "addresses_info"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    address: Mapped[str]
    location: Mapped[str]
    apartment: Mapped[str] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)
    entrance: Mapped[str] = mapped_column(nullable=True)
    floor: Mapped[str] = mapped_column(nullable=True)
