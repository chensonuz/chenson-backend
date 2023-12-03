import os
import sys
from typing import Any, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.event import listens_for
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.dependencies import UnitOfWorkDep
from app.uow import UnitOfWork
from core.database.db import get_session, Base
from core.exceptions.handlers import add_exception_handlers
from core.routers import add_app_routers
from tests.utils import generate_init_data, TestConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


# This fixture is the main difference to before. It creates a nested
# transaction, recreates it when the application code calls session.commit
# and rolls it back at the end.
# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
async def session():
    connection = await test_engine.connect()
    transaction = connection.begin()
    session = test_async_session(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @listens_for(session, "after_transaction_end")
    async def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = await connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    await transaction.rollback()
    await connection.close()


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
async def uow() -> Generator[UnitOfWorkDep, Any, None]:
    _uow: UnitOfWorkDep = UnitOfWork()
    _uow.session_factory = test_async_session
    yield _uow


@pytest.fixture
async def app(
    uow: UnitOfWorkDep, session: AsyncSession
) -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """

    def override_get_db():
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    _app = start_app()
    # await create_fixtures(uow)
    async with LifespanManager(_app):
        _app.dependency_overrides[uow] = uow
        _app.dependency_overrides[get_session] = override_get_db
        yield _app


#
@pytest.fixture
async def client(app: FastAPI) -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(
        app=app,
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def authorized_client(app: FastAPI) -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(
        app=app,
        headers={
            "Content-Type": "application/json",
            "Authorization": generate_init_data()[1],
        },
    ) as client:
        yield client
