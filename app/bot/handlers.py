from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from loguru import logger

from app.bot.dependencies import get_bot_instance
from app.user.service import UserService
from core.config import AppConfig

bot = get_bot_instance()


async def start_handler(message: Message):
    photo_url = await UserService.get_user_profile_photos(
        bot, message.from_user.id
    )
    logger.warning(photo_url)
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
