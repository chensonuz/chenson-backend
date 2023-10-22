from sqlalchemy import Column

from app.user.database.models import User
from core.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_one(self, id: int, **kwargs):
        return await super().find_one(id, options=[])

    async def find_one_or_none(self, id: int, **kwargs):
        return await super().find_one_or_none(id, options=[])

    async def find_one_by(self, column: Column, value, **kwargs):
        return await super().find_one_by(column, value, options=[])

    async def find_one_by_telegram_id(self, value, **kwargs):
        return await super().find_one_by(
            self.model.telegram_id, value, options=[]
        )

    async def find_one_or_none_by(self, column: Column, value, **kwargs):
        return await super().find_one_or_none_by(column, value, options=[])

    async def find_one_or_none_by_telegram_id(self, value, **kwargs):
        return await super().find_one_or_none_by(
            self.model.telegram_id, value, options=[]
        )

    async def find_all(self, **kwargs):
        return await super().find_all(**kwargs)
