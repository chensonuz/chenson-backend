from loguru import logger

from app.category.admin.schemas import (
    AdminCategoryCreateRequest,
    AdminCategoryUpdateRequest,
    AdminCategoryUpdatePartialRequest,
)
from app.category.schemas import CategoryResponse
from app.dependencies import UnitOfWorkDep


class AdminCategoryService:
    @staticmethod
    async def create(
        uow: UnitOfWorkDep, data: AdminCategoryCreateRequest
    ) -> int | str:
        return await uow.admin_category.add_one(data.model_dump())

    @staticmethod
    async def update(
        uow: UnitOfWorkDep, id: int | str, data: AdminCategoryUpdateRequest
    ) -> None:
        logger.info(await uow.admin_category.update_one(id, data.model_dump()))

    @staticmethod
    async def update_partial(
        uow: UnitOfWorkDep,
        id: int | str,
        data: AdminCategoryUpdatePartialRequest,
    ) -> None:
        logger.info(
            await uow.admin_category.update_one(
                id, data.model_dump(exclude_unset=True)
            )
        )

    @staticmethod
    async def delete(uow: UnitOfWorkDep, id: int | str) -> None:
        logger.info(await uow.admin_category.delete_one(id))

    @staticmethod
    async def get_all(uow: UnitOfWorkDep) -> list[CategoryResponse]:
        response = await uow.admin_category.find_all()
        return [CategoryResponse.model_validate(item) for item in response]

    @staticmethod
    async def get(uow: UnitOfWorkDep, id: int | str) -> CategoryResponse | None:
        response = await uow.admin_category.find_one_or_none(id)
        if response:
            return CategoryResponse.model_validate(response)
