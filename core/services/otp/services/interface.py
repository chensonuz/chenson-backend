from datetime import datetime
from typing import Optional, Dict

from core.services.otp.exceptions import (
    LimitExceededError,
    TOO_MANY_SMS_ATTEMPTS,
)
from core.services.otp.schemas import (
    SMSInfoWithPhone,
    SendSMSRequest,
    SendSMSResponse,
)


class StorageManager:
    def __init__(self):
        self.__storage: Dict[str, int] = {}

    def get_sms_attempts_by_number(self, phone_number: str) -> int:
        cache_data = self.__storage.get(phone_number)

        if not cache_data:
            return 0

        return self.__storage[phone_number]


class SendSMSService:
    __max_sms_attempts = 5

    def __init__(self, sms_data: SendSMSRequest):
        self.sms_data = sms_data
        self.__storage_manager = StorageManager()

    def get_new_phone_store_data(
        self, code: Optional[str] = None
    ) -> SMSInfoWithPhone:
        return SMSInfoWithPhone(
            sms_code=code,
            phone_number=self.sms_data.phone_number,
            timestamp=datetime.utcnow().timestamp(),
        )

    async def __check_sms_attempts_limit(self):
        current_attempts = self.__storage_manager.get_sms_attempts_by_number(
            phone_number=self.sms_data.phone_number
        )

        if current_attempts >= self.__max_sms_attempts:
            raise LimitExceededError(TOO_MANY_SMS_ATTEMPTS)

    async def send_sms_code(self) -> SendSMSResponse:
        raise NotImplementedError("Interface Method")
