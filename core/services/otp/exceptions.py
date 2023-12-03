from pydantic import BaseModel


class ErrorMessage(BaseModel):
    message: str = "Error Occurred"
    codeError: str = "undefinedError"


TOO_MANY_SMS_ATTEMPTS = ErrorMessage(
    message="Too many attempts. Try again later", codeError="limitSMSExceeded"
)


class AppException(Exception):
    def __init__(self, name: ErrorMessage):
        self.name = name


class LimitExceededError(AppException):
    pass
