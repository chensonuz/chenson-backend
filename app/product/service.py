from typing import List

from sqlalchemy.orm import joinedload

from app.product.filters import ProductFilter
from app.product.models import Product
from app.product.schemas import ProductResponse
from core.exceptions.classes import NotFoundError
from core.services.uow import AbstractUnitOfWork


class ProductService:
    """
    Category service

    This service is responsible for category-related operations

    List of responsibilities:
    - get category
    - get categories
    - get category children
    """

    @staticmethod
    async def get_products_for_category(
        uow: AbstractUnitOfWork, category_id: int
    ) -> List[ProductResponse]:
        """
        Get products for specific category

        This method is used to get products from the database by category id. If
        category doesn't exist, empty list is returned.

        :param uow: unit of work instance
        :param id: id as integer
        :return: product view model
        """
        async with uow:
            products = await uow.product.find_all_by_category_id(category_id)
            return [
                ProductResponse.model_validate(product) for product in products
            ]

    @staticmethod
    async def get_products(
        uow: AbstractUnitOfWork, filter_: ProductFilter | None = None
    ) -> List[ProductResponse]:
        """
        Get products

        This method is used to get products from the database. If
        products don't exist, empty list is returned.

        :param filter_: filter instance
        :param uow: unit of work instance
        :return: product view model
        """
        async with uow:
            products = await uow.product.find_all(
                filter=filter_, options=[joinedload(Product.category)]
            )
            return [
                ProductResponse.model_validate(product) for product in products
            ]

    @staticmethod
    async def get_product(uow: AbstractUnitOfWork, id: int) -> ProductResponse:
        """
        Get product

        This method is used to get a product from the database by id. If
        product doesn't exist, exception is raised.

        :param uow: unit of work instance
        :param id: id as integer
        :return: category view model
        """
        async with uow:
            product = await uow.product.find_one_or_none(id)
            if not product:
                raise NotFoundError("Product not found")
            return ProductResponse.model_validate(product)
