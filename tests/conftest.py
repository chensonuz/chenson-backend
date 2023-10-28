import os
import sys
from typing import Any, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.dependencies import UnitOfWorkDep
from app.uow import UnitOfWork
from app.user.router import router as user_router
from core.config._main import _Config
from core.database.db import get_session, Base
from core.exceptions.handlers import add_exception_handlers
from core.fixtures import create_fixtures
from core.routers import add_app_routers

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TestConfig = _Config()


test_engine = create_async_engine(
    TestConfig.SQLALCHEMY_TEST_DATABASE_URI.unicode_string(),
    echo=TestConfig.SQLALCHEMY_DEBUG,
    future=True,
)


test_async_session = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(params=["asyncio"], scope="session")
def anyio_backend(request):
    return request.param


async def get_test_session() -> Generator[AsyncSession, Any, None]:
    async with test_async_session() as session, session.begin():
        yield session


def start_app() -> FastAPI:
    TestConfig.RUN_BOT_POLLING = False

    app = FastAPI()
    app.include_router(user_router)
    return app


@pytest.fixture(scope="session")
async def uow() -> Generator[UnitOfWorkDep, Any, None]:
    _uow: UnitOfWorkDep = UnitOfWork()
    _uow.session_factory = test_async_session
    yield _uow


@pytest.fixture
async def app(uow: UnitOfWorkDep) -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _app = start_app()
    add_exception_handlers(_app)
    add_app_routers(_app)
    await create_fixtures(uow)
    async with LifespanManager(_app):
        yield _app
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


#
@pytest.fixture
async def client(
    app: FastAPI, uow: UnitOfWorkDep
) -> Generator[AsyncClient, Any, None]:
    app.dependency_overrides[uow] = uow
    app.dependency_overrides[get_session] = get_test_session
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
