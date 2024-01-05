"""Routers for order app."""

from fastapi import APIRouter, Depends

from app.dependencies import auth_service, get_current_user, UnitOfWorkDep
from app.order.schemas import OrderCreateRequest, OrderResponse
from app.order.service import OrderService
from app.user.schemas import UserResponse

router = APIRouter(dependencies=[Depends(auth_service)])


@router.post("/checkout", status_code=201)
async def checkout_order(
    uow: UnitOfWorkDep,
    data: OrderCreateRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> int:
    """Checkout endpoint."""
    return await OrderService.checkout_order(uow, data, current_user)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    uow: UnitOfWorkDep,
    order_id: int,
):
    """Get order endpoint."""
    return await OrderService.get_order(uow, order_id)


@router.get("", response_model=list[OrderResponse])
async def get_orders(
    uow: UnitOfWorkDep,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get orders endpoint."""
    return await OrderService.get_orders(uow, current_user.id)
