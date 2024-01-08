"""Routers for order app."""

from fastapi import APIRouter, Depends

from app.dependencies import auth_service, get_current_user, UnitOfWorkDep
from app.order.schemas import (
    OrderCreateRequest,
    APIOrderListResponse,
    APIOrderResponse,
)
from app.order.service import OrderService
from app.user.schemas import UserResponse
from core.schemas.base import APIResponseID, APIResponseWithID

router = APIRouter(dependencies=[Depends(auth_service)])


@router.post("/checkout", status_code=201, response_model=APIResponseWithID)
async def checkout_order(
    uow: UnitOfWorkDep,
    data: OrderCreateRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> APIResponseWithID:
    """Checkout endpoint."""
    created_id = await OrderService.checkout_order(uow, data, current_user)
    return APIResponseWithID(
        success=True,
        message="Order created successfully",
        data=APIResponseID(id=created_id),
    )


@router.get("/{order_id}", response_model=APIOrderResponse)
async def get_order(
    uow: UnitOfWorkDep,
    order_id: int,
) -> APIOrderResponse:
    """Get order endpoint."""
    return APIOrderResponse(
        success=True,
        message="Order retrieved.",
        data=await OrderService.get_order(uow, order_id),
    )


@router.get("", response_model=APIOrderListResponse)
async def get_orders(
    uow: UnitOfWorkDep,
    current_user: UserResponse = Depends(get_current_user),
) -> APIOrderListResponse:
    """Get orders endpoint."""
    return APIOrderListResponse(
        success=True,
        message="Orders retrieved.",
        data=await OrderService.get_orders(uow, current_user.id),
    )
