import pytest
from httpx import AsyncClient

from app.admin.schemas import AdminUserBaseWithPassword
from app.category.admin.schemas import AdminCategoryCreateRequest
from app.user.models import UserRole
from app.user.utils import hash_password
from tests.utils import TestConfig, TestUnitOfWorkDep

__all__ = ["admin_token", "create_superuser"]


@pytest.fixture(scope="session")
async def create_superuser(override_uow: TestUnitOfWorkDep) -> int:
    admin_user = AdminUserBaseWithPassword(
        email=TestConfig.FIRST_SUPERUSER,
        password=hash_password(TestConfig.FIRST_SUPERUSER_PASSWORD),
        role=UserRole.Admin,
    )
    async with override_uow:
        if not await override_uow.admin_user.find_one_or_none_by_email(
            admin_user.email
        ):
            return await override_uow.admin_user.add_one(
                admin_user.model_dump(exclude_none=True)
            )


@pytest.fixture(scope="session")
async def admin_token(client: AsyncClient, create_superuser: int):
    response = await client.post(
        "/api/v1/admin/auth",
        json={
            "email": TestConfig.FIRST_SUPERUSER,
            "password": TestConfig.FIRST_SUPERUSER_PASSWORD,
        },
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["access_token"] is not None
    return response_data["access_token"]
