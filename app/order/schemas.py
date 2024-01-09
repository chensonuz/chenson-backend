"""Order schemas module."""
from typing import List

from pydantic import BaseModel

from app.order.constants import OrderStatus, PaymentMethod
from app.product.schemas import ProductResponse, OrderProductResponse
from app.user.schemas import UserResponse, UserShortResponse
from core.schemas.base import BaseORMSchema, APIResponse


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemID(BaseModel):
    id: int


class OrderItemResponse(BaseORMSchema, OrderItemID, OrderItemBase):
    product: ProductResponse


class OrderItemShortResponse(BaseORMSchema, OrderItemID, OrderItemBase):
    product: OrderProductResponse


class OrderItemCreateRequest(OrderItemBase):
    product_id: int
    quantity: int


class OrderItemCreateDB(OrderItemCreateRequest):
    order_id: int


class OrderBase(BaseModel):
    user_id: int
    amount: float
    address_info_id: int
    payment_method: PaymentMethod
    status: OrderStatus | None = OrderStatus.ACCEPTED

    def display_status(self) -> str:
        return OrderStatus(self.status).display_name()

    def display_payment_method(self) -> str:
        return PaymentMethod(self.payment_method).display_name()


class OrderID(BaseModel):
    id: int


class OrderResponse(BaseORMSchema, OrderID, OrderBase):
    client: UserResponse
    items: List[OrderItemResponse]


class OrderShortResponse(BaseORMSchema, OrderID, OrderBase):
    client: UserShortResponse
    items: List[OrderItemShortResponse]


class AddressInfo(BaseORMSchema):
    address: str
    location: str
    apartment: str | None = None
    comment: str | None = None
    entrance: str | None = None
    floor: str | None = None

    def address_link(self) -> str:
        return f"<a href='https://www.google.com/maps/search/?api=1&query={self.location}'>{self.address}</a>"


class OrderCreateRequest(BaseModel):
    address_info: AddressInfo
    payment_method: PaymentMethod
    status: OrderStatus | None = OrderStatus.ACCEPTED
    items: List[OrderItemCreateRequest]


class OrderCreateDB(OrderBase):
    user_id: int
    payment_method: PaymentMethod


class APIOrderResponse(APIResponse):
    data: OrderShortResponse


class APIOrderListResponse(APIResponse):
    data: List[OrderShortResponse]
