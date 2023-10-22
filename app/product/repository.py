from typing import List

from sqlalchemy import Column

from app.product.models import Product
from core.repositories.base import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def find_one(self, id: int, **kwargs) -> model:
        return await super().find_one(id, options=[])

    async def find_one_or_none(self, id: int, **kwargs) -> model | None:
        return await super().find_one_or_none(id, options=[])

    async def find_one_by(self, column: Column, value, **kwargs) -> model:
        return await super().find_one_by(column, value, options=[])

    async def find_one_or_none_by(
        self, column: Column, value, **kwargs
    ) -> model | None:
        return await super().find_one_or_none_by(column, value, options=[])

    async def find_all(self, **kwargs) -> list[model]:
        return await super().find_all(**kwargs)

    async def find_all_by_category_id(self, value, **kwargs) -> list[model]:
        return await super().find_all_by(
            self.model.category_id, value, **kwargs
        )

    async def find_all_by_filter(
        self, filters: List[bool | None], **kwargs
    ) -> list[model]:
        return await super().find_all_by_filter(filters, **kwargs)
