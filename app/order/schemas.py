"""Order schemas module."""
from typing import List

from pydantic import BaseModel

from app.order.constants import OrderStatus, PaymentMethod
from app.product.schemas import ProductResponse
from app.user.schemas import UserResponse
from core.schemas.base import BaseORMSchema


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemID(BaseModel):
    id: int


class OrderItemResponse(BaseORMSchema, OrderItemID, OrderItemBase):
    product: ProductResponse


class OrderItemCreateRequest(OrderItemBase):
    product_id: int
    quantity: int


class OrderItemCreateDB(OrderItemCreateRequest):
    order_id: int


class OrderBase(BaseModel):
    user_id: int
    amount: int
    address_info_id: int
    status: OrderStatus | None = OrderStatus.ACCEPTED


class OrderID(BaseModel):
    id: int


class OrderResponse(BaseORMSchema, OrderID, OrderBase):
    client: UserResponse
    items: List[OrderItemResponse]


class AddressInfo(BaseModel):
    address: str
    location: str
    apartment: str | None = None
    comment: str | None = None
    entrance: str | None = None
    floor: str | None = None


class OrderCreateRequest(BaseModel):
    address_info: AddressInfo
    payment_method: PaymentMethod
    status: OrderStatus | None = OrderStatus.ACCEPTED
    items: List[OrderItemCreateRequest]


class OrderCreateDB(OrderBase):
    user_id: int
    payment_method: PaymentMethod
