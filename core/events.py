import asyncio

from aiogram import Dispatcher, Bot
from fastapi import FastAPI

from core.fixture import init_models, create_fixtures


def add_events(app: FastAPI, **kwargs):
    @app.on_event("startup")
    async def startup():
        # create Bot dispatcher
        bot: Bot = kwargs.get("bot")
        bot_dispatcher: Dispatcher = kwargs.get("bot_dispatcher")
        if bot and bot_dispatcher:
            asyncio.create_task(bot_dispatcher.start_polling(bot))
        # create db tables
        await init_models()
        await create_fixtures()

    @app.on_event("shutdown")
    async def shutdown():
        bot_dispatcher: Dispatcher = kwargs.get("bot_dispatcher")
        if bot_dispatcher:
            await bot_dispatcher.stop_polling()
