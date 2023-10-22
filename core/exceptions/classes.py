from typing import Union

from fastapi import HTTPException

from core.schemas.base import APIResponse


class APIException(HTTPException):
    pass


class BaseAppError(Exception):
    def __init__(self, message: Union[APIResponse, str]):
        self.response = (
            APIResponse(success=False, message=message, data=None)
            if isinstance(message, str)
            else message
        )


class NotFoundError(BaseAppError):
    pass


class ConflictError(BaseAppError):
    pass


class UnauthorizedError(BaseAppError):
    pass


class ValuePydanticError(BaseAppError):
    pass


class TwilioError(BaseAppError):
    pass


class ForbiddenError(BaseAppError):
    pass


class TerraSmsError(BaseAppError):
    pass


class BadPhoneCodeError(BaseAppError):
    pass


class PhoneError(BaseAppError):
    pass


class RetrySmsError(BaseAppError):
    pass


class OrderStatusError(BaseAppError):
    pass


class UnprocessableEntityError(BaseAppError):
    pass


class RequestError(BaseAppError):
    pass


class InternalError(BaseAppError):
    pass


class IntegrationError(BaseAppError):
    pass
