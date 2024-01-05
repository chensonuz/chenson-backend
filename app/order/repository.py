"""Order repository module."""
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.order.models import Order, OrderItem
from core.repositories.base import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def find_one_or_none(self, id: str | int, **kwargs):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(joinedload(Order.client), joinedload(Order.items))
        )
        res = await self.session.execute(stmt)
        return res.unique().scalar_one_or_none()

    async def find_all_by_user_id(self, value, **kwargs) -> list[model]:
        return await super().find_all_by(
            self.model.user_id,
            value,
            options=[
                joinedload(self.model.client),
                joinedload(self.model.address_info),
                joinedload(self.model.items),
            ],
        )


class OrderItemRepository(SQLAlchemyRepository):
    model = OrderItem
