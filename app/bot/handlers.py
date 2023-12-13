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
        text="_Welcome!_",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Open Calendar",
                        web_app=WebAppInfo(url=AppConfig.BOT_WEB_APP_HOST),
                    )
                ]
            ]
        ),
        parse_mode="Markdown",
    )
