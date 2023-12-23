from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.category.models import Category
from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class Product(Base, CreatedUpdatedMixin):
    __tablename__ = "products"
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    status: Mapped[bool] = mapped_column(default=True)
    category: Mapped["Category"] = relationship(lazy="joined")
    images: Mapped[List["ProductImage"]] = relationship(
        back_populates="product"
    )


class ProductImage(Base, CreatedUpdatedMixin):
    __tablename__ = "product_images"
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE")
    )
    image: Mapped[str]
    product: Mapped["Product"] = relationship(back_populates="images")
