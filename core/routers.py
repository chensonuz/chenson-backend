from fastapi import FastAPI

from app.admin.router import router as admin_router
from app.category.admin.router import router as admin_categories_router
from app.category.router import router as categories_router
from app.order.admin.router import router as admin_orders_router
from app.order.router import router as orders_router
from app.product.admin.router import router as admin_products_router
from app.product.router import router as products_router
from app.user.admin.router import router as admin_users_router
from app.user.router import router as users_router
from core.config import AppConfig
from core.logging.logger import init_logging


def add_app_routers(app: FastAPI):
    init_logging()

    @app.get("/health", name="main:health")
    def healthcheck():
        return {"message": "OK"}

    app.include_router(
        router=users_router,
        prefix=f"{AppConfig.PREFIX}/users",
        tags=["users"],
    )

    app.include_router(
        router=admin_users_router,
        prefix=f"{AppConfig.PREFIX}/admin/users",
        tags=["admin_users"],
    )

    app.include_router(
        router=categories_router,
        prefix=f"{AppConfig.PREFIX}/categories",
        tags=["categories"],
    )

    app.include_router(
        router=admin_categories_router,
        prefix=f"{AppConfig.PREFIX}/admin/categories",
        tags=["admin_categories"],
    )

    app.include_router(
        router=products_router,
        prefix=f"{AppConfig.PREFIX}/products",
        tags=["products"],
    )

    app.include_router(
        router=admin_products_router,
        prefix=f"{AppConfig.PREFIX}/admin/products",
        tags=["admin_products"],
    )

    app.include_router(
        router=orders_router,
        prefix=f"{AppConfig.PREFIX}/orders",
        tags=["orders"],
    )

    app.include_router(
        router=admin_orders_router,
        prefix=f"{AppConfig.PREFIX}/admin/orders",
        tags=["admin_orders"],
    )

    app.include_router(
        router=admin_router,
        prefix=f"{AppConfig.PREFIX}/admin",
        tags=["admin"],
    )
