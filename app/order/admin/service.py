from typing import List

from sqlalchemy.orm import subqueryload

from app.dependencies import UnitOfWorkDep
from app.order.admin.schemas import (
    AdminOrderCreateRequest,
    AdminOrderUpdateRequest,
)
from app.order.models import Order
from app.order.schemas import OrderResponse
from core.exceptions.classes import NotFoundError


class AdminOrderService:
    """Admin Order Service

    This service is responsible for admin-order-related operations

    List of responsibilities:
    - create order
    - update order
    - delete order
    - get all orders
    - get order
    """

    @staticmethod
    async def create(
        uow: UnitOfWorkDep, data: AdminOrderCreateRequest
    ) -> int | str:
        """Create new order

        This method is used to create new order

        :param uow: unit of work instance
        :param data: order view model
        :return: order id
        """
        async with uow:
            return await uow.order.add_one(data.model_dump())

    @staticmethod
    async def update(
        uow: UnitOfWorkDep,
        id: int,
        data: AdminOrderUpdateRequest,
    ) -> int:
        """Update order by id

        This method is used to update order by id

        :param uow: unit of work instance
        :param id: order id
        :param data: order view model
        """
        async with uow:
            if not await uow.order.find_one_or_none(id):
                raise NotFoundError(message="Order not found")
            return await uow.order.update_one(
                id, data.model_dump(exclude_unset=True)
            )

    @staticmethod
    async def delete(uow: UnitOfWorkDep, id: int) -> int:
        """Delete order by id

        This method is used to delete order by id

        :param uow: unit of work instance
        :param id: order id
        :return: order id
        """
        async with uow:
            if not await uow.order.find_one_or_none(id):
                raise NotFoundError(message="Order not found")
            return await uow.order.delete_one(id)

    @staticmethod
    async def get_all(uow: UnitOfWorkDep) -> List[OrderResponse]:
        """Get all orders

        This method is used to get all orders

        :param uow: unit of work instance
        :return: list of orders
        """
        async with uow:
            return [
                OrderResponse.model_validate(item)
                for item in await uow.order.find_all(
                    options=[
                        subqueryload(Order.client),
                        subqueryload(Order.items),
                    ]
                )
            ]

    @staticmethod
    async def get(uow: UnitOfWorkDep, id: int) -> OrderResponse:
        """Get order by id

        This method is used to get order by id

        :param uow: unit of work instance
        :param id: order id
        :return: order
        """
        async with uow:
            item = await uow.order.find_one_or_none(id)
            if not item:
                raise NotFoundError(message="Order not found")
            return OrderResponse.model_validate(item)
