"""Order service module."""
from typing import List

from app.order.schemas import (
    OrderCreateRequest,
    OrderCreateDB,
    OrderItemCreateDB,
    OrderShortResponse,
)
from app.uow import UnitOfWork
from app.user.schemas import UserResponse
from core.exceptions.classes import NotFoundError


class OrderService:
    """Order service class.

    Service for order app."""

    @staticmethod
    async def checkout_order(
        uow: UnitOfWork, data: OrderCreateRequest, current_user: UserResponse
    ) -> int:
        """Checkout order method.

        :param uow: unit of work instance
        :param data: order data
        :param current_user: current user
        :return: order response
        """
        async with uow:
            filtered_order_items = []
            order_item_prices = []

            products = await uow.product.find_all_in_ids(
                [item.product_id for item in data.items]
            )

            for order_item, product in zip(data.items, products):
                if not product:
                    continue
                if not product.status:
                    continue
                filtered_order_items.append(order_item)
                order_item_prices.append(order_item.quantity * product.price)

            if not filtered_order_items:
                raise NotFoundError("No products found for order")

            order_id = await uow.order.add_one(
                OrderCreateDB(
                    user_id=current_user.id,
                    address_info_id=data.address_info_id,
                    amount=sum(order_item_prices),
                    status=data.status,
                    payment_method=data.payment_method,
                ).model_dump(),
                commit=False,
            )
            order_items = [
                OrderItemCreateDB(
                    order_id=order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                ).model_dump()
                for item in filtered_order_items
            ]
            await uow.order_item.add_many(
                order_items,
                commit=False,
            )
            await uow.commit()
            return order_id

    @staticmethod
    async def get_order(uow: UnitOfWork, order_id: int) -> OrderShortResponse:
        """Get order method.

        :param uow: unit of work instance
        :param order_id: order id
        :return: order response
        """
        async with uow:
            order = await uow.order.find_one_or_none(order_id)
            if not order:
                raise NotFoundError("Order not found")
            return OrderShortResponse.model_validate(order)

    @staticmethod
    async def get_orders(
        uow: UnitOfWork, user_id: int
    ) -> List[OrderShortResponse]:
        """Get orders method.

        :param user_id: user id
        :param uow: unit of work instance
        :return: list of order responses
        """
        async with uow:
            data = await uow.order.find_all_by_user_id(user_id)
            return [OrderShortResponse.model_validate(order) for order in data]
