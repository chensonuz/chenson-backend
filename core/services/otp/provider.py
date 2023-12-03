from core.config import AppConfig
from core.services.otp.schemas import SendSMSRequest
from core.services.otp.services.interface import SendSMSService
from core.services.otp.services.mock import SendSMSServiceMock


class OTPServiceProvider:
    phones_white_list = {"+998900631455"}

    @staticmethod
    def provide_send_sms_service(data: SendSMSRequest) -> SendSMSService:
        if (
            data.phone_number in OTPServiceProvider.phones_white_list
            or AppConfig.DEBUG
        ):
            return SendSMSServiceMock(sms_data=data)

        return SendSMSServiceMock(sms_data=data)
