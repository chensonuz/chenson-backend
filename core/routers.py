from fastapi import FastAPI

from app.user.routes import router
from core.config import AppConfig
from core.logging.logger import init_logging


def add_app_routers(app: FastAPI):
    init_logging()

    @app.get("/health")
    def healthcheck():
        return {"message": "OK"}

    app.include_router(
        router=router,
        prefix=f"{AppConfig.PREFIX}/user",
        tags=["user"],
    )
