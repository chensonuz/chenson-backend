from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel


class APIException(HTTPException):
    pass


class ErrorMessage(BaseModel):
    message: str = "Error Occurred"
    codeError: str


class BaseAppError(Exception):
    def __init__(self, name: Union[ErrorMessage, str]):
        self.name = (
            ErrorMessage(message=name, codeError="undefined")
            if isinstance(name, str)
            else name
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
