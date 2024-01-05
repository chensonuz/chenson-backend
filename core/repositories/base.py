from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import insert, select, Column, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.classes import ConflictError


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all_by(self, column, value):
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_filter(self, filters: List[bool | None]):
        raise NotImplementedError

    @abstractmethod
    def find_one(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_one_or_none(self, id):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id, data, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by(self, column, value):
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none_by(self, column, value):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_many(self, data: list[dict]) -> list[str | int]:
        stmt = insert(self.model).returning(self.model.id)
        try:
            res = await self.session.execute(stmt, data)
            await self.session.commit()
            return list(map(int, res.scalars().all()))
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ConflictError(str(e)) from e

    async def add_one(self, data: dict) -> str | int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        try:
            res = await self.session.execute(stmt)
            await self.session.commit()
            return res.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ConflictError(str(e)) from e

    async def find_all(self, **kwargs):
        stmt = select(self.model)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        if "filter" in kwargs:
            stmt = kwargs["filter"].filter(stmt)
            stmt = kwargs["filter"].sort(stmt)
        res = await self.session.execute(stmt)
        return [row[0] for row in res.unique().all()]

    async def find_all_by(self, column: Column, value, **kwargs) -> list[model]:
        stmt = select(self.model).where(column == value)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        res = await self.session.execute(stmt)
        return [row[0] for row in res.unique().all()]

    async def find_all_by_filter(
        self, filters: List[bool | None], **kwargs
    ) -> list[model]:
        stmt = select(self.model)
        if filters:
            for f in filters:
                if f is not None:
                    stmt = stmt.where(f)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def find_one(self, id: str | int, **kwargs) -> model:
        stmt = select(self.model).where(self.model.id == id)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except SQLAlchemyError as e:
            raise ConflictError(str(e)) from e

    async def find_one_or_none(self, id: str | int, **kwargs):
        stmt = select(self.model).where(self.model.id == id)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_one(self, id: str | int, data: dict, **kwargs):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model.id)
        )
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        try:
            res = await self.session.execute(stmt)
            await self.session.commit()
            return res.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ConflictError(str(e)) from e

    async def delete_one(self, id: str | int):
        stmt = (
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model.id)
        )
        try:
            res = await self.session.execute(stmt)
            await self.session.commit()
            return res.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ConflictError(str(e)) from e

    async def delete_many(self, ids: list[str | int]):
        stmt = (
            delete(self.model)
            .where(self.model.id.in_(ids))
            .returning(self.model.id)
        )
        try:
            res = await self.session.execute(stmt)
            await self.session.commit()
            return list(map(int, res.scalars().all()))
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ConflictError(str(e)) from e

    async def find_one_by(self, column: Column, value, **kwargs) -> model:
        stmt = select(self.model).where(column == value)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except SQLAlchemyError as e:
            raise ConflictError(str(e)) from e

    async def find_one_by_filter(self, filters: List[bool | None]) -> model:
        stmt = select(self.model)
        if filters:
            for f in filters:
                if f is not None:
                    stmt = stmt.where(f)
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except SQLAlchemyError as e:
            raise ConflictError(str(e)) from e

    async def find_one_or_none_by(self, column: Column, value, **kwargs):
        stmt = select(self.model).where(column == value)
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
