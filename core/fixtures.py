import random

from faker import Faker

from app.category.admin.schemas import AdminCategoryCreateRequest
from app.dependencies import UnitOfWorkDep
from app.product.schemas import ProductCreate
from app.user.admin.schemas import (
    AdminUserBaseWithPassword,
)
from app.user.models import UserRole
from app.user.utils import hash_password
from core.config import AppConfig
from core.database.db import engine, Base


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_fixtures(uow: UnitOfWorkDep):
    fake = Faker()
    async with uow:
        admin_user = AdminUserBaseWithPassword(
            email=AppConfig.FIRST_SUPERUSER,
            password=hash_password(AppConfig.FIRST_SUPERUSER_PASSWORD),
            role=UserRole.Admin,
        )
        await uow.admin_user.add_one(admin_user.model_dump(exclude_none=True))
        await uow.commit()
    async with uow:
        for _ in range(5):
            cat_obj = AdminCategoryCreateRequest(
                title=fake.text(max_nb_chars=10).replace(".", ""), status=True
            )
            category_id = await uow.category.add_one(
                cat_obj.model_dump(exclude_none=True)
            )
            await uow.commit()
            for _ in range(random.randint(0, 10)):
                product_obj = ProductCreate(
                    category_id=category_id,
                    title=fake.text(max_nb_chars=10).replace(".", ""),
                    description=fake.text(max_nb_chars=50),
                    price=random.randint(1000, 30000),
                    status=True,
                )
                await uow.product.add_one(
                    product_obj.model_dump(exclude_none=True)
                )
                await uow.commit()
