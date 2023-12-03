from datetime import datetime

from pydantic import BaseModel


class SMSInfo(BaseModel):
    sms_code: str | None = None
    timestamp: float = datetime.utcnow().timestamp()
    sms_attempts: int = 1


class SMSInfoWithPhone(SMSInfo):
    phone_number: str


class SendSMSRequest(BaseModel):
    phone_number: str


class SendSMSResponse(BaseModel):
    success: bool


class ValidateCodeRequest(BaseModel):
    phone_number: str
    code: str


class ValidateCodeResponse(BaseModel):
    success: bool
