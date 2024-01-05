"""Order service module."""
from typing import List

from app.order.schemas import (
    OrderCreateRequest,
    OrderResponse,
    OrderCreateDB,
    OrderItemCreateDB,
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
            address_info = data.address_info.model_dump()
            address_info["user_id"] = current_user.id
            address_info_id = await uow.address_info.add_one(address_info)

            order_id = await uow.order.add_one(
                OrderCreateDB(
                    user_id=current_user.id,
                    address_info_id=address_info_id,
                    amount=sum(order_item_prices),
                    status=data.status,
                    payment_method=data.payment_method,
                ).model_dump()
            )

            await uow.order_item.add_many(
                [
                    OrderItemCreateDB(
                        order_id=order_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                    ).model_dump()
                    for item in filtered_order_items
                ]
            )
            return order_id  # await OrderService.get_order(uow, order_id)

    @staticmethod
    async def get_order(uow: UnitOfWork, order_id: int) -> OrderResponse:
        """Get order method.

        :param uow: unit of work instance
        :param order_id: order id
        :return: order response
        """
        async with uow:
            order = await uow.order.find_one_or_none(order_id)
            if not order:
                raise NotFoundError("Order not found")
            # order_items = [
            #     OrderItemResponse.model_validate(item) for item in order.items
            # ]
            # client = UserResponse.model_validate(order.client)
            # return OrderResponse(
            #     **order.model_dump(exclude={"items", "client"}),
            #     client=client,
            #     items=order_items,
            # )
            return OrderResponse.model_validate(order)

    @staticmethod
    async def get_orders(uow: UnitOfWork, user_id: int) -> List[OrderResponse]:
        """Get orders method.

        :param user_id: user id
        :param uow: unit of work instance
        :return: list of order responses
        """
        async with uow:
            return [
                OrderResponse.model_validate(order)
                for order in await uow.order.find_all_by_user_id(user_id)
            ]
