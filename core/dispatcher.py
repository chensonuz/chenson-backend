from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand

from app.bot.handlers import start_handler


def add_bot_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(
        start_handler,
        Command(BotCommand(command="start", description="Start the bot")),
    )
