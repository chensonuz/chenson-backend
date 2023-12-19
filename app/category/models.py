from sqlalchemy.orm import Mapped, mapped_column

from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class Category(Base, CreatedUpdatedMixin):
    __tablename__ = "categories"

    title: Mapped[str]
    status: Mapped[bool] = mapped_column(default=True)
