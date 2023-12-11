import os
import sys
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.uow import UnitOfWork
from core.database.db import Base, get_session
from core.exceptions.handlers import add_exception_handlers
from core.routers import add_app_routers
from tests.utils import (
    TestConfig,
    TestUnitOfWork,
    TestUnitOfWorkDep,
    generate_init_data,
    test_async_session,
    test_engine,
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(params=["asyncio"], scope="session")
def anyio_backend(request):
    return request.param


@pytest.fixture(params=["asyncio"], scope="session")
async def get_test_session() -> Generator[AsyncSession, Any, None]:
    async with test_async_session() as session, session.begin():
        yield session


def start_app() -> FastAPI:
    TestConfig.RUN_BOT_POLLING = False

    app = FastAPI()
    add_exception_handlers(app)
    add_app_routers(app)
    return app


@pytest.fixture(scope="session")
async def override_uow() -> Generator[TestUnitOfWorkDep, Any, None]:
    yield TestUnitOfWork()


@pytest.fixture(scope="session")
async def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield start_app()


#
@pytest.fixture(scope="session")
async def client(
    app: FastAPI,
    override_uow: TestUnitOfWorkDep,
    get_test_session: AsyncSession,
) -> Generator[AsyncClient, Any, None]:
    app.dependency_overrides[UnitOfWork] = TestUnitOfWork
    app.dependency_overrides[get_session] = get_test_session
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def authorized_client(app: FastAPI) -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={
            "Content-Type": "application/json",
            "Authorization": generate_init_data()[1],
        },
    ) as client:
        yield client


from tests.fixtures import *  # noqa


@pytest.fixture
async def admin_client(
    app: FastAPI, admin_token: str
) -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}",
        },
    ) as client:
        yield client
