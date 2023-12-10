from typing import List

from app.category.admin.schemas import (
    AdminCategoryCreateRequest,
    AdminCategoryUpdateRequest,
)
from app.category.schemas import CategoryResponse
from app.dependencies import UnitOfWorkDep
from core.exceptions.classes import NotFoundError, ConflictError


class AdminCategoryService:
    """Admin Category service

    This service is responsible for admin-category-related operations

    List of responsibilities:
    - create category
    - update category
    - delete category
    - get all categories
    - get category
    """

    @staticmethod
    async def create(
        uow: UnitOfWorkDep, data: AdminCategoryCreateRequest
    ) -> int | str:
        """Create new category

        This method is used to create new category

        :param uow: unit of work instance
        :param data: category view model
        :return: category id
        """
        async with uow:
            return await uow.category.add_one(data.model_dump())

    @staticmethod
    async def update(
        uow: UnitOfWorkDep,
        id: int,
        data: AdminCategoryUpdateRequest,
    ) -> int:
        """Update category by id

        This method is used to update category by id

        :param uow: unit of work instance
        :param id: category id
        :param data: category view model
        """
        async with uow:
            if not await uow.category.find_one_or_none(id):
                raise NotFoundError(message="Category not found")
            return await uow.category.update_one(
                id, data.model_dump(exclude_unset=True)
            )

    @staticmethod
    async def delete(uow: UnitOfWorkDep, id: int) -> int:
        """Delete category by id

        This method is used to delete category by id

        :param uow: unit of work instance
        :param id: category id
        :return: category id
        """
        async with uow:
            if not await uow.category.find_one_or_none(id):
                raise NotFoundError(message="Category not found")
            if await uow.product.find_all_by_category_id(id):
                raise ConflictError(
                    message="Category has children. Delete them first"
                )
            return await uow.category.delete_one(id)

    @staticmethod
    async def get_all(uow: UnitOfWorkDep) -> List[CategoryResponse]:
        """Get all categories

        This method is used to get all categories

        :param uow: unit of work instance
        :return: list of categories
        """
        async with uow:
            response = await uow.category.find_all()
            return [CategoryResponse.model_validate(item) for item in response]

    @staticmethod
    async def get(uow: UnitOfWorkDep, id: int) -> CategoryResponse:
        """Get category by id

        This method is used to get category by id

        :param uow: unit of work instance
        :param id: category id
        :return: category
        """
        async with uow:
            response = await uow.category.find_one_or_none(id)
            if not response:
                raise NotFoundError(message="Category not found")
            return CategoryResponse.model_validate(response)
