from typing import List

from app.category.schemas import CategoryResponse
from core.services.uow import AbstractUnitOfWork


class CategoryService:
    """
    Category service

    This service is responsible for category-related operations

    List of responsibilities:
    - get category
    - get categories
    - get category children
    """

    @staticmethod
    async def get_category(
        uow: AbstractUnitOfWork, id: int
    ) -> CategoryResponse | None:
        """
        Get category

        This method is used to get a category from the database by id. If
        category doesn't exist, None is returned.

        :param uow: unit of work instance
        :param id: id as integer
        :return: category view model
        """
        async with uow:
            category = await uow.category.find_one(id)
            return CategoryResponse.model_validate(category)

    @staticmethod
    async def get_categories(uow: AbstractUnitOfWork) -> List[CategoryResponse]:
        """
        Get categories

        This method is used to get all categories from the database.

        :param uow: unit of work instance
        :return: list of category view models
        """
        async with uow:
            categories = await uow.category.find_all_by_filter(filters=[])
            return [
                CategoryResponse.model_validate(category)
                for category in categories
            ]
