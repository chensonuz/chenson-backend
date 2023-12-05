from sqlalchemy.orm import Mapped

from app.user.models import UserRole
from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class AdminUser(Base, CreatedUpdatedMixin):
    __tablename__ = "admins"

    role: Mapped[UserRole]
    email: Mapped[str | None]
    password: Mapped[str]
