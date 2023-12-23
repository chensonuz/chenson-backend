import asyncio

from aiogram import Dispatcher, Bot
from fastapi import FastAPI

from core.config import AppConfig
from core.fixtures import init_models


def add_events(app: FastAPI, **kwargs):
    @app.on_event("startup")
    async def startup():
        # create Bot dispatcher
        bot: Bot = kwargs.get("bot")
        bot_dispatcher: Dispatcher = kwargs.get("bot_dispatcher")
        if bot and bot_dispatcher and AppConfig.RUN_BOT_POLLING:
            asyncio.create_task(bot_dispatcher.start_polling(bot))
        # create db tables
        await init_models()

    @app.on_event("shutdown")
    async def shutdown():
        bot_dispatcher: Dispatcher = kwargs.get("bot_dispatcher")
        if bot_dispatcher and AppConfig.RUN_BOT_POLLING:
            await bot_dispatcher.stop_polling()
