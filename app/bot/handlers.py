from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

from app.bot.dependencies import get_bot_instance
from core.config import AppConfig

bot = get_bot_instance()


async def start_handler(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Ознакомьтесь с нашим меню с помощью кнопок ниже.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Открыть меню [PROD]",
                        web_app=WebAppInfo(url=AppConfig.BOT_WEB_APP_HOST),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Открыть меню [DEV]",
                        web_app=WebAppInfo(url=AppConfig.BOT_WEB_APP_DEV_HOST),
                    )
                ],
            ]
        ),
        parse_mode="Markdown",
    )
