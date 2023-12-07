from fastapi import APIRouter, Depends

from app.category.admin.schemas import (
    AdminCategoryCreateRequest,
    AdminCategoryUpdateRequest,
)
from app.category.admin.service import AdminCategoryService
from app.category.schemas import (
    APICategoryListResponse,
    APICategoryResponse,
)
from app.dependencies import UnitOfWorkDep
from app.permissions import is_admin
from core.schemas.base import APIResponseWithID, APIResponseID

router = APIRouter(dependencies=[Depends(is_admin)])


@router.get("", response_model=APICategoryListResponse)
async def category_get_all(uow: UnitOfWorkDep):
    response = await AdminCategoryService.get_all(uow=uow)
    return APICategoryListResponse(
        success=True, message="Categories retrieved.", data=response
    )


@router.get("/{category_id}", response_model=APICategoryResponse)
async def category_get(category_id: int, uow: UnitOfWorkDep):
    response = await AdminCategoryService.get(uow=uow, id=category_id)
    return APICategoryResponse(
        success=response is not None,
        message="Category retrieved." if response else "Category not found",
        data=response,
    )


@router.post("", response_model=APIResponseWithID, status_code=201)
async def category_create(
    request: AdminCategoryCreateRequest, uow: UnitOfWorkDep
):
    created_id = await AdminCategoryService.create(uow=uow, data=request)
    return APIResponseWithID(
        success=True,
        message="Category created.",
        data=APIResponseID(id=created_id),
    )


@router.patch("/{category_id}", response_model=APIResponseWithID)
async def category_update(
    category_id: int,
    request: AdminCategoryUpdateRequest,
    uow: UnitOfWorkDep,
):
    updated_id = await AdminCategoryService.update(
        uow=uow, id=category_id, data=request
    )
    return APIResponseWithID(
        success=True,
        message="Category updated.",
        data=APIResponseID(id=updated_id),
    )


@router.delete("/{category_id}", response_model=APIResponseWithID)
async def category_delete(category_id: int, uow: UnitOfWorkDep):
    deleted_id = await AdminCategoryService.delete(uow=uow, id=category_id)
    return APIResponseWithID(
        success=True,
        message="Category deleted.",
        data=APIResponseID(id=deleted_id),
    )
