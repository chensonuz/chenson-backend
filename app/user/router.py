from fastapi import APIRouter, Depends

from app.user import mapper
from app.dependencies import auth_service, UnitOfWorkDep, get_current_user
from app.user.schemas import UserResponse
from app.user.service import UserService
from core.schemas.base import APIDetailedResponse
from core.services.auth import AuthService

router = APIRouter()

APIResponse = APIDetailedResponse(UserResponse)


@router.post("/auth", response_model=APIResponse)
async def user_auth(
    uow: UnitOfWorkDep, auth: AuthService = Depends(auth_service)
) -> APIResponse:
    """
    User authentication

    This method is used to authenticate a user. If user doesn't exist, it is created.

    :param uow: unit of work instance
    :param auth: auth service
    :return: api response with user data
    """
    user = await UserService.get_user(uow, auth.init_data.user.id)
    if not user:
        await UserService.register_user(
            uow, mapper.auth_data_to_create_schema(auth.init_data)
        )
        user = await UserService.get_user(uow, auth.init_data.user.id)

    return APIResponse(success=True, message="User authenticated", data=user)


@router.get("/me", response_model=APIResponse)
async def user_me(
    current_user: UserResponse = Depends(get_current_user),
) -> APIResponse:
    return APIResponse(success=True, message="Your data", data=current_user)
