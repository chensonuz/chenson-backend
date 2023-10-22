import asyncio

from aiogram import Dispatcher, Bot
from fastapi import FastAPI

from core.database.db import engine, Base


def add_events(app: FastAPI, **kwargs):
    @app.on_event("startup")
    async def startup():
        # create Bot dispatcher
        bot: Bot = kwargs.get("bot")
        bot_dispatcher: Dispatcher = kwargs.get("bot_dispatcher")
        if bot and bot_dispatcher:
            asyncio.create_task(bot_dispatcher.start_polling(bot))
        # create db tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown():
        bot_dispatcher: Dispatcher = kwargs.get("bot_dispatcher")
        if bot_dispatcher:
            await bot_dispatcher.stop_polling()
