from typing import List

from sqlalchemy.orm import joinedload

from app.dependencies import UnitOfWorkDep
from app.product import mapper
from app.product.admin.schemas import (
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
)
from app.product.models import Product
from app.product.schemas import ProductResponse
from app.utils.images import (
    delete_file,
    create_product_images,
)
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
            product_id = await uow.product.add_one(
                data.model_dump(exclude={"images"})
            )
            images_data = create_product_images(data.images, product_id)
            await uow.product_image.add_many(data=images_data)
            return product_id

    @staticmethod
    async def update(
        uow: UnitOfWorkDep, id: int, data: AdminProductUpdateRequest
    ) -> int:
        """Update product

        This method is used to update product

        :param uow: unit of work instance
        :param id: product id
        :param data: product view model
        :return: product id
        """
        async with uow:
            current_product = await uow.product.find_one_or_none(id)
            if not current_product:
                raise NotFoundError(message="Product not found")
            if data.images:
                if data.images.to_be_created:
                    images_to_create = create_product_images(
                        data.images.to_be_created,
                        current_product.id,
                    )
                    await uow.product_image.add_many(data=images_to_create)
                if data.images.to_be_deleted:
                    await uow.product_image.delete_many(
                        data.images.to_be_deleted
                    )
                    for image_id in data.images.to_be_deleted:
                        image = await uow.product_image.find_one_or_none(
                            image_id
                        )
                        if image:
                            delete_file(image.image)
            return await uow.product.update_one(
                id, data.model_dump(exclude_unset=True, exclude={"images"})
            )

    @staticmethod
    async def delete(uow: UnitOfWorkDep, id: int) -> int:
        """Delete product

        This method is used to delete product

        :param uow: unit of work instance
        :param id: Product ID
        :return: product id
        """
        async with uow:
            if not await uow.product.find_one_or_none(id):
                raise NotFoundError(message="Product not found")
            return await uow.product.delete_one(id)

    @staticmethod
    async def get_all(uow: UnitOfWorkDep) -> List[ProductResponse]:
        """Get all products

        This method is used to get all products

        :param uow: unit of work instance
        :return: list of products
        """
        async with uow:
            products = await uow.product.find_all(
                options=[joinedload(Product.images)]
            )
            return [mapper.db_to_domain(product) for product in products]

    @staticmethod
    async def get(uow: UnitOfWorkDep, id: int) -> ProductResponse:
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
