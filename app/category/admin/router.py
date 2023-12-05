from fastapi import APIRouter, Depends

from app.category.admin.schemas import (
    AdminCategoryUpdatePartialRequest,
    AdminCategoryCreateRequest,
)
from app.category.admin.service import AdminCategoryService
from app.category.schemas import (
    APICategoryListResponse,
    APICategoryResponse,
    APICategoryCreatedResponse,
)
from app.dependencies import UnitOfWorkDep
from app.permissions import is_admin
from core.schemas.base import APIResponse

router = APIRouter(dependencies=[Depends(is_admin)])


@router.get("/", response_model=APICategoryListResponse)
async def category_get_all(uow: UnitOfWorkDep):
    response = await AdminCategoryService.get_all(uow=uow)
    return APICategoryListResponse(
        success=True, message="Categories retrieved.", data=response
    )


@router.get("/{category_id}", response_model=APICategoryResponse)
async def category_get(category_id: int | str, uow: UnitOfWorkDep):
    response = await AdminCategoryService.get(uow=uow, id=category_id)
    return APICategoryResponse(
        success=response is not None,
        message="Category retrieved." if response else "Category not found",
        data=response,
    )


@router.post("/", response_model=APICategoryCreatedResponse)
async def category_create(
    request: AdminCategoryCreateRequest, uow: UnitOfWorkDep
):
    response = await AdminCategoryService.create(uow=uow, data=request)
    return (
        APICategoryCreatedResponse(
            success=True, message="Category created.", data=response
        ),
        201,
    )


@router.patch("/{category_id}", response_model=APIResponse)
async def category_update(
    category_id: int | str,
    request: AdminCategoryUpdatePartialRequest,
    uow: UnitOfWorkDep,
):
    await AdminCategoryService.update_partial(
        uow=uow, id=category_id, data=request
    )
    return APIResponse(success=True, message="Category updated.")


@router.delete("/{category_id}")
async def category_delete(
    category_id: int | str,
    uow: UnitOfWorkDep,
):
    await AdminCategoryService.delete(uow=uow, id=category_id)
    return APIResponse(success=True, message="Category deleted.")
