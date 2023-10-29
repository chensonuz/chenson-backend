import base64
import hashlib
import hmac
import random
import string
import urllib.parse
from datetime import datetime
from typing import Tuple

from app.user.schemas import TelegramUser
from core.config._main import _Config

TestConfig = _Config()


def generate_init_data(
    tg_user: TelegramUser | None = None,
) -> Tuple[TelegramUser, str]:
    query_id = "".join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(24)
    )
    if not tg_user:
        tg_user = TelegramUser(
            id=int(
                "".join(
                    random.SystemRandom().choice(string.digits)
                    for _ in range(10)
                )
            ),
            first_name="Test",
            last_name="Testov",
            username="testtestov",
            language_code="en",
            added_to_attachment_menu=True,
        )
    bot_token = (
        TestConfig.BOT_TOKEN
        if not TestConfig.BOT_TEST_ENVIRONMENT
        else TestConfig.TEST_BOT_TOKEN
    )

    fake_data = {
        "query_id": query_id,
        "user": tg_user.model_dump_json(exclude_unset=True, exclude_none=True),
        "auth_date": int(datetime.utcnow().timestamp()),
    }
    data_check_string = "\n".join(
        sorted([f"{k}={v}" for k, v in fake_data.items()])
    )
    secret_key = hmac.new(
        b"WebAppData", bot_token.encode(), hashlib.sha256
    ).digest()
    data_signature = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    fake_data["hash"] = data_signature
    fake_encoded_data = urllib.parse.urlencode(fake_data)
    return tg_user, base64.b64encode(fake_encoded_data.encode()).decode()
