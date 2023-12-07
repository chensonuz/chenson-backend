from fastapi import APIRouter, Depends

from app.dependencies import UnitOfWorkDep
from app.permissions import is_admin
from app.user.admin.schemas import (
    AdminUserCreateRequest,
    AdminUserUpdateRequest,
)
from app.user.admin.service import AdminUserService
from app.user.schemas import APIUserListResponse, APIUserResponse
from core.schemas.base import APIResponseWithID, APIResponseID

router = APIRouter(dependencies=[Depends(is_admin)])


@router.get("", response_model=APIUserListResponse)
async def admin_get_users(uow: UnitOfWorkDep):
    return APIUserListResponse(
        success=True,
        message="Users retrieved.",
        data=await AdminUserService.get_all_users(uow=uow),
    )


@router.get("/{user_id}", response_model=APIUserResponse)
async def admin_get_user(user_id: int, uow: UnitOfWorkDep):
    return APIUserResponse(
        success=True,
        message="User retrieved.",
        data=await AdminUserService.get_user(uow=uow, id=user_id),
    )


@router.post("", response_model=APIResponseWithID, status_code=201)
async def admin_create_user(
    request: AdminUserCreateRequest, uow: UnitOfWorkDep
):
    created_id = await AdminUserService.create_user(uow=uow, request=request)
    return APIResponseWithID(
        success=True,
        message="User created.",
        data=APIResponseID(id=created_id),
    )


@router.patch("/{user_id}", response_model=APIResponseWithID)
async def admin_update_user(
    user_id: int, request: AdminUserUpdateRequest, uow: UnitOfWorkDep
):
    updated_id = await AdminUserService.update_user(
        uow=uow, id=user_id, request=request
    )
    return APIResponseWithID(
        success=True,
        message="User updated.",
        data=APIResponseID(id=updated_id),
    )


@router.delete("/{user_id}", response_model=APIResponseWithID)
async def admin_delete_user(user_id: int, uow: UnitOfWorkDep):
    deleted_id = await AdminUserService.delete_user(uow=uow, id=user_id)
    return APIResponseWithID(
        success=True,
        message="User deleted.",
        data=APIResponseID(id=deleted_id),
    )
