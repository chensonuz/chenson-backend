from typing import Annotated

from fastapi import Depends

from app.uow import UnitOfWork
from app.user.schemas import UserResponse
from app.user.service import UserService
from core.config import AppConfig
from core.exceptions.classes import APIException, NotFoundError
from core.schemas.base import APIResponse
from core.services.auth import AuthService
from core.services.uow import AbstractUnitOfWork

UnitOfWorkDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]
auth_service = AuthService(
    AppConfig.TEST_BOT_TOKEN
    if AppConfig.BOT_TEST_ENVIRONMENT
    else AppConfig.BOT_TOKEN
)


async def get_current_user(
    uow: UnitOfWorkDep, auth: AuthService = Depends(auth_service)
) -> UserResponse:
    user = await UserService.get_user(uow, auth.init_data.user.id)
    if not user:
        raise APIException(
            status_code=404,
            detail=APIResponse(success=False, message="User not found"),
        )
    return user


async def get_target_user(user_id: int | str, uow: UnitOfWorkDep) -> int | str:
    user = await UserService.get_user(uow, user_id)
    if not user:
        raise NotFoundError(message="User not found")
    return user.id
