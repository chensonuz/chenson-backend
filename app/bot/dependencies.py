from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from core.config import AppConfig


def get_bot_instance() -> Bot:
    environment_path = "test/" if AppConfig.BOT_TEST_ENVIRONMENT else ""
    session = AiohttpSession(
        api=TelegramAPIServer(
            base=f"https://api.telegram.org/bot{{token}}/{environment_path}{{method}}",
            file=f"https://api.telegram.org/file/bot{{token}}{environment_path}/{{path}}",
        )
    )

    token = (
        AppConfig.TEST_BOT_TOKEN
        if AppConfig.BOT_TEST_ENVIRONMENT
        else AppConfig.BOT_TOKEN
    )

    bot = Bot(token=token, session=session)
    return bot
