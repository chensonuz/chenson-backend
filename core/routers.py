from fastapi import FastAPI

from app.category.router import router as categories_router
from app.product.router import router as products_router
from app.user.router import router as users_router
from core.config import AppConfig
from core.logging.logger import init_logging


def add_app_routers(app: FastAPI):
    init_logging()

    @app.get("/health")
    def healthcheck():
        return {"message": "OK"}

    app.include_router(
        router=users_router,
        prefix=f"{AppConfig.PREFIX}/users",
        tags=["users"],
    )

    app.include_router(
        router=categories_router,
        prefix=f"{AppConfig.PREFIX}/categories",
        tags=["categories"],
    )

    app.include_router(
        router=products_router,
        prefix=f"{AppConfig.PREFIX}/products",
        tags=["products"],
    )
