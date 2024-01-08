from typing import List

from pydantic import BaseModel

from app.order.constants import PaymentMethod, OrderStatus
from app.order.schemas import (
    OrderCreateRequest,
    AddressInfo,
    OrderItemCreateRequest,
    OrderResponse,
)
from core.schemas.base import APIResponse


class AdminOrderCreateRequest(OrderCreateRequest):
    address_info: AddressInfo = AddressInfo(
        address="Sayram 5th Drive, 17B",
        location="41.326565, 69.316100",
        comment="Podval",
        entrance="2",
        floor="-1",
    )
    payment_method: PaymentMethod = PaymentMethod.CASH


class AdminOrderUpdateRequest(BaseModel):
    address_info: AddressInfo | None = None
    payment_method: PaymentMethod | None = None
    status: OrderStatus | None = None
    items: List[OrderItemCreateRequest] | None = None


class APIAdminOrderResponse(APIResponse):
    data: OrderResponse


class APIAdminOrderListResponse(APIResponse):
    data: List[OrderResponse]
