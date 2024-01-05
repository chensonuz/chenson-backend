from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.product.models import Product, ProductImage
from app.utils.images import delete_file
from core.exceptions.classes import ConflictError
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

    async def find_all_in_ids(self, ids: list[int], **kwargs) -> list[model]:
        stmt = select(self.model).where(self.model.id.in_(ids))
        if "options" in kwargs:
            for option in kwargs["options"]:
                stmt = stmt.options(option)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_all_by_category_id(self, value, **kwargs) -> list[model]:
        return await super().find_all_by(
            self.model.category_id, value, **kwargs
        )


class ProductImageRepository(SQLAlchemyRepository):
    model = ProductImage

    async def delete_many(self, ids: list[int | str]) -> None:
        stmt = (
            delete(self.model)
            .where(self.model.id.in_(ids))
            .returning(self.model.image)
        )
        try:
            res = await self.session.execute(stmt)
            await self.session.commit()
            image_paths = res.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ConflictError(str(e)) from e

        for image_path in image_paths:
            delete_file(image_path)
        return
