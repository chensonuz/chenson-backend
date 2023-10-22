from typing import Annotated

from fastapi import Depends

from core.services.uow import AbstractUnitOfWork
from app.user.schemas import UserResponse
from core.services.auth import AuthService
from app.uow import UnitOfWork
from app.user.service import UserService
from core.config import AppConfig
from core.exceptions.classes import APIException
from core.schemas.base import APIResponse

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