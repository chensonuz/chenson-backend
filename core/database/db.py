from loguru import logger
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import AppConfig

DATABASE_URL = AppConfig.SQLALCHEMY_DATABASE_URI.unicode_string()

engine = create_async_engine(
    DATABASE_URL, echo=AppConfig.SQLALCHEMY_DEBUG, future=True
)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session, session.begin():
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(e)


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base = declarative_base()
Base.metadata = MetaData(naming_convention=convention)
