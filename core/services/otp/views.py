from loguru import logger

from core.services.otp.provider import OTPServiceProvider
from core.services.otp.schemas import (
    SendSMSRequest,
    SendSMSResponse,
    ValidateCodeRequest,
    ValidateCodeResponse,
)


async def send_sms(data: dict) -> SendSMSResponse:
    try:
        sms_info = SendSMSRequest.model_validate(data)
        service = OTPServiceProvider.provide_send_sms_service(data=sms_info)
        return await service.send_sms_code()
    except Exception as e:
        logger.error(f"Error sending message: {e}")


async def validate_sms(data: dict) -> ValidateCodeResponse:
    sms_info = ValidateCodeRequest.model_validate(data)
    return ValidateCodeResponse(success=True)
