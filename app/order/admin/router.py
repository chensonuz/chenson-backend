from fastapi import APIRouter, Depends

from app.dependencies import UnitOfWorkDep
from app.order.admin.schemas import (
    APIAdminOrderListResponse,
    APIAdminOrderResponse,
)
from app.order.admin.schemas import (
    AdminOrderCreateRequest,
    AdminOrderUpdateRequest,
)
from app.order.admin.service import AdminOrderService
from app.permissions import is_admin
from core.schemas.base import APIResponseWithID, APIResponseID

router = APIRouter(dependencies=[Depends(is_admin)])


@router.get("", response_model=APIAdminOrderListResponse)
async def admin_order_get_all(uow: UnitOfWorkDep):
    response = await AdminOrderService.get_all(uow=uow)
    return APIAdminOrderListResponse(
        success=True, message="Orders retrieved.", data=response
    )


@router.get("/{order_id}", response_model=APIAdminOrderResponse)
async def admin_order_get(order_id: int, uow: UnitOfWorkDep):
    response = await AdminOrderService.get(uow=uow, id=order_id)
    return APIAdminOrderResponse(
        success=response is not None,
        message="Order retrieved." if response else "Order not found",
        data=response,
    )


@router.post("", response_model=APIResponseWithID, status_code=201)
async def admin_order_create(
    request: AdminOrderCreateRequest, uow: UnitOfWorkDep
):
    created_id = await AdminOrderService.create(uow=uow, data=request)
    return APIResponseWithID(
        success=True,
        message="Order created.",
        data=APIResponseID(id=created_id),
    )


@router.patch("/{order_id}", response_model=APIResponseWithID)
async def admin_order_update(
    order_id: int,
    request: AdminOrderUpdateRequest,
    uow: UnitOfWorkDep,
):
    updated_id = await AdminOrderService.update(
        uow=uow, id=order_id, data=request
    )
    return APIResponseWithID(
        success=True,
        message="Order updated.",
        data=APIResponseID(id=updated_id),
    )


@router.delete("/{order_id}", response_model=APIResponseWithID)
async def admin_order_delete(order_id: int, uow: UnitOfWorkDep):
    deleted_id = await AdminOrderService.delete(uow=uow, id=order_id)
    return APIResponseWithID(
        success=True,
        message="Order deleted.",
        data=APIResponseID(id=deleted_id),
    )
