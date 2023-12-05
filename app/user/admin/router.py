from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import UnitOfWorkDep, get_target_user
from app.permissions import is_admin
from app.user.admin.schemas import (
    AdminUserCreateRequest,
    AdminUserUpdateRequest,
)
from app.user.admin.service import AdminUserService
from app.user.schemas import APIUserListResponse, APIUserResponse
from core.schemas.base import APIResponse

router = APIRouter(dependencies=[Depends(is_admin)])


@router.get("", response_model=APIUserListResponse)
async def admin_get_users(uow: UnitOfWorkDep):
    return APIUserListResponse(
        success=True,
        message="Users retrieved.",
        data=await AdminUserService.get_all_users(uow=uow),
    )


@router.get("/{user_id}", response_model=APIUserResponse)
async def admin_get_user(user_id: int | str, uow: UnitOfWorkDep):
    return APIUserResponse(
        success=True,
        message="User retrieved.",
        data=await AdminUserService.get_user(uow=uow, id=user_id),
    )


@router.post("", response_model=APIUserResponse)
async def admin_create_user(
    request: AdminUserCreateRequest,
    uow: UnitOfWorkDep,
):
    return (
        APIUserResponse(
            success=True,
            message="User created.",
            data=await AdminUserService.create_user(uow=uow, request=request),
        ),
        201,
    )


@router.patch("/{user_id}", response_model=APIUserResponse)
async def admin_update_user(
    request: AdminUserUpdateRequest,
    target_user_id: Annotated[int | str, Depends(get_target_user)],
    uow: UnitOfWorkDep,
):
    return APIUserResponse(
        success=True,
        message="User updated.",
        data=await AdminUserService.update_user(
            uow=uow, id=target_user_id, request=request
        ),
    )


@router.delete("/{user_id}", response_model=APIResponse)
async def admin_delete_user(
    target_user_id: Annotated[int | str, Depends(get_target_user)],
    uow: UnitOfWorkDep,
):
    await AdminUserService.delete_user(uow=uow, id=target_user_id)
    return APIResponse(success=True, message="User deleted.")
