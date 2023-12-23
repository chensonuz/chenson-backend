from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.product.models import Product, ProductImage
from core.repositories.base import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def find_one_or_none(self, id: str | int, **kwargs):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(joinedload(Product.images))
        )
        res = await self.session.execute(stmt)
        return res.unique().scalar_one_or_none()

    async def find_all_by_category_id(self, value, **kwargs) -> list[model]:
        return await super().find_all_by(
            self.model.category_id, value, **kwargs
        )


class ProductImageRepository(SQLAlchemyRepository):
    model = ProductImage
