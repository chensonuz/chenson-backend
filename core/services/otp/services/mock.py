from core.services.otp.schemas import SendSMSRequest, SendSMSResponse
from core.services.otp.services.interface import SendSMSService


class SendSMSServiceMock(SendSMSService):
    def __init__(self, sms_data: SendSMSRequest):
        super().__init__(sms_data=sms_data)

    async def send_sms_code(self) -> SendSMSResponse:
        return SendSMSResponse(success=True)
