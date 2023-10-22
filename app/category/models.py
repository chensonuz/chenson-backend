from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.product.models import Product
from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class Category(Base, CreatedUpdatedMixin):
    __tablename__ = "categories"

    title: Mapped[str]
    status: Mapped[bool] = mapped_column(default=True)
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categories.id")
    )
    children: Mapped["Category"] = relationship("Category")
    products: Mapped["Product"] = relationship("Product")
