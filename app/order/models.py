"""Order models module."""
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.order.constants import OrderStatus, PaymentMethod
from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin

if TYPE_CHECKING:
    from app.product.models import Product
    from app.user.models import User, AddressInfo


class OrderItem(Base, CreatedUpdatedMixin):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    product: Mapped["Product"] = relationship("Product", lazy="selectin")


class Order(Base, CreatedUpdatedMixin):
    __tablename__ = "orders"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    address_info_id: Mapped[int] = mapped_column(
        ForeignKey("addresses_info.id")
    )
    amount: Mapped[int]
    payment_method: Mapped[PaymentMethod]
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.ACCEPTED)
    client: Mapped["User"] = relationship("User")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem")
    address_info: Mapped["AddressInfo"] = relationship(
        "AddressInfo", lazy="selectin"
    )
