from typing import List

from app.dependencies import UnitOfWorkDep
from app.product.admin.schemas import (
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
)
from app.product.schemas import ProductResponse
from core.exceptions.classes import NotFoundError


class AdminProductService:
    """Admin Product service

    This service is responsible for admin-product-related operations

    List of responsibilities:
    - create product
    - update product
    - delete product
    - get all products
    - get product
    """

    @staticmethod
    async def create(
        uow: UnitOfWorkDep, data: AdminProductCreateRequest
    ) -> int | str:
        """Create new product

        This method is used to create new product

        :param uow: unit of work instance
        :param data: product view model
        :return: product id
        """
        async with uow:
            return await uow.product.add_one(data.model_dump())

    @staticmethod
    async def update(
        uow: UnitOfWorkDep, id: int | str, data: AdminProductUpdateRequest
    ) -> None:
        """Update product

        This method is used to update product

        :param uow: unit of work instance
        :param id: product id
        :param data: product view model
        :return: product id
        """
        async with uow:
            if not await uow.product.find_one_or_none(id):
                raise NotFoundError(message="Product not found")
            await uow.product.update_one(
                id, data.model_dump(exclude_unset=True)
            )

    @staticmethod
    async def delete(uow: UnitOfWorkDep, id: int | str) -> None:
        """Delete product

        This method is used to delete product

        :param uow: unit of work instance
        :param id: Product ID
        :return: product id
        """
        async with uow:
            if not await uow.product.find_one_or_none(id):
                raise NotFoundError(message="Product not found")
            await uow.product.delete_one(id)

    @staticmethod
    async def get_all(uow: UnitOfWorkDep) -> List[ProductResponse]:
        """Get all products

        This method is used to get all products

        :param uow: unit of work instance
        :return: list of products
        """
        async with uow:
            products = await uow.product.find_all()
            return [
                ProductResponse.model_validate(product) for product in products
            ]

    @staticmethod
    async def get(uow: UnitOfWorkDep, id: int | str) -> ProductResponse:
        """Get product by id

        This method is used to get product by id

        :param uow: unit of work instance
        :param id: product id
        :return: product
        """
        async with uow:
            product = await uow.product.find_one_or_none(id)
            if not product:
                raise NotFoundError(message="Product not found")
            return ProductResponse.model_validate(product)
