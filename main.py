import uvicorn
from aiogram import Dispatcher
from fastapi import FastAPI

from app.bot.dependencies import get_bot_instance
from core.config import AppConfig, get_swagger_config
from core.dispatcher import add_bot_handlers
from core.events import add_events
from core.exceptions.handlers import add_exception_handlers
from core.logging.logger import init_logging
from core.middleware import add_middleware
from core.routers import add_app_routers


def create_app() -> FastAPI:
    app = FastAPI(**get_swagger_config())
    bot = get_bot_instance()
    bot_dispatcher = Dispatcher()

    init_logging()

    # Error handling
    add_exception_handlers(app)

    add_events(app, bot_dispatcher=bot_dispatcher, bot=bot)

    # Middleware
    add_middleware(app)

    # Add Pagination
    # add_pagination(app)

    # Register bot handlers
    add_bot_handlers(bot_dispatcher)

    # Static Files
    # app.mount("/media", StaticFiles(directory="media"), name="media")

    # Routers
    add_app_routers(app)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        port=AppConfig.PORT,
        host="0.0.0.0",
        reload=False,
        factory=True,
    )
