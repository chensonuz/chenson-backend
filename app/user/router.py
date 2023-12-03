from fastapi import APIRouter, Depends
from loguru import logger

from app.dependencies import auth_service, UnitOfWorkDep, get_current_user
from app.user import mapper
from app.user.schemas import (
    UserResponse,
    UserSignInUpResponse,
    RequestSMSRequest,
)
from app.user.service import UserService
from core.exceptions.classes import APIException
from core.schemas.base import APIDetailedResponse
from core.services import otp
from core.services.auth import AuthService

router = APIRouter()

APIUserResponse = APIDetailedResponse(UserResponse)
APIRequestSMSResponse = APIDetailedResponse(None)
APISignInUpResponse = APIDetailedResponse(UserSignInUpResponse)


@router.post("/auth", name="user:auth", response_model=APISignInUpResponse)
async def user_auth(
    uow: UnitOfWorkDep, auth: AuthService = Depends(auth_service)
) -> APISignInUpResponse:
    """
    User authentication

    This method is used to authenticate a user. If user doesn't exist, it is created.

    :param uow: unit of work instance
    :param auth: auth service
    :return: api response with user data
    """
    user = await UserService.get_user(uow, auth.init_data.user.id)
    created = False
    logger.info(f"1, {auth.init_data.user.id}, {created}")
    if not user:
        await UserService.register_user(
            uow, mapper.auth_data_to_create_schema(auth.init_data)
        )
        created = True
        user = await UserService.get_user(uow, auth.init_data.user.id)
        logger.info(f"2, {auth.init_data.user.id}, {created}")

    return APISignInUpResponse(
        success=True,
        message="User authenticated",
        data=UserSignInUpResponse(created=created, user=user),
    )


@router.post(
    "/request-sms",
    name="user:request_sms",
    response_model=APIRequestSMSResponse,
)
async def request_otp_sms(
    data: RequestSMSRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    try:
        service_response = await otp.send_sms(data.model_dump())
        if not service_response:
            raise APIException(
                status_code=400, detail=str(service_response.success)
            )
        return APIRequestSMSResponse(success=True, message="SMS code sent")
    except Exception as exc:
        raise APIException(status_code=400, detail=str(exc))


@router.get("/me", name="user:me", response_model=APIUserResponse)
async def user_me(
    current_user: UserResponse = Depends(get_current_user),
) -> APIUserResponse:
    return APIUserResponse(success=True, message="Your data", data=current_user)
