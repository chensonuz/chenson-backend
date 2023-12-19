from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.category.models import Category
from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class Product(Base, CreatedUpdatedMixin):
    __tablename__ = "products"
    category_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categories.id")
    )
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    status: Mapped[bool] = mapped_column(default=True)
    category: Mapped["Category"] = relationship("Category", lazy="joined")
