from fastapi import APIRouter, Depends

from app.dependencies import UnitOfWorkDep
from app.permissions import is_admin
from app.product.admin.schemas import (
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
)
from app.product.admin.service import AdminProductService
from app.product.schemas import APIProductListResponse, APIProductResponse
from core.schemas.base import (
    APIResponseID,
    APIResponseWithID,
)

router = APIRouter(dependencies=[Depends(is_admin)])


@router.get("", response_model=APIProductListResponse)
async def admin_get_products(uow: UnitOfWorkDep):
    return APIProductListResponse(
        success=True,
        message="Products retrieved.",
        data=await AdminProductService.get_all(uow=uow),
    )


@router.post("", response_model=APIResponseWithID, status_code=201)
async def admin_create_product(
    uow: UnitOfWorkDep, data: AdminProductCreateRequest
):
    created_id = await AdminProductService.create(uow=uow, data=data)
    return APIResponseWithID(
        success=True,
        message="Product created.",
        data=APIResponseID(id=created_id),
    )


@router.patch("/{product_id}", response_model=APIResponseWithID)
async def admin_update_product(
    uow: UnitOfWorkDep, product_id: int, data: AdminProductUpdateRequest
):
    updated_id = await AdminProductService.update(
        uow=uow, id=product_id, data=data
    )
    return APIResponseWithID(
        success=True,
        message="Product updated.",
        data=APIResponseID(id=updated_id),
    )


@router.delete("/{product_id}", response_model=APIResponseWithID)
async def admin_delete_product(uow: UnitOfWorkDep, product_id: int):
    deleted_id = await AdminProductService.delete(uow=uow, id=product_id)
    return APIResponseWithID(
        success=True,
        message="Product deleted.",
        data=APIResponseID(id=deleted_id),
    )


@router.get("/{product_id}", response_model=APIProductResponse)
async def admin_get_product(uow: UnitOfWorkDep, product_id: int):
    return APIProductResponse(
        success=True,
        message="Product retrieved.",
        data=await AdminProductService.get(uow=uow, id=product_id),
    )
