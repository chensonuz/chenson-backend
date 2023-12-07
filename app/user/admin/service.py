from typing import List

from app.user.admin.schemas import (
    AdminUserUpdateRequest,
    AdminUserCreateRequest,
)
from app.user.schemas import UserResponse
from core.exceptions.classes import NotFoundError
from core.services.uow import AbstractUnitOfWork


class AdminUserService:
    """
    Admin User service

    This service is responsible for admin-user-related operations

    List of responsibilities:
    - get all users
    - get user by id
    - create user
    - update user by id
    - delete user by id
    """

    @staticmethod
    async def get_all_users(uow: AbstractUnitOfWork) -> List[UserResponse]:
        """
        Get all users

        This method is used to get all users

        :param uow: unit of work instance
        :return: list of users
        """
        async with uow:
            users = await uow.user.find_all()
            return [UserResponse.model_validate(user) for user in users]

    @staticmethod
    async def get_user(uow: AbstractUnitOfWork, id: int) -> UserResponse:
        """
        Get user by id

        This method is used to get user by id

        :param uow: unit of work instance
        :param id: user id
        :return: user
        """
        async with uow:
            user = await uow.user.find_one_or_none(id)
            if not user:
                raise NotFoundError(message="User not found")
            return UserResponse.model_validate(user)

    @staticmethod
    async def create_user(
        uow: AbstractUnitOfWork, request: AdminUserCreateRequest
    ) -> int | str:
        """
        Create user

        This method is used to create user

        :param uow: unit of work instance
        :param request: user view model
        :return: user
        """
        async with uow:
            return await uow.user.add_one(request.model_dump())

    @staticmethod
    async def update_user(
        uow: AbstractUnitOfWork, id: int, request: AdminUserUpdateRequest
    ) -> None:
        """
        Update user by id

        This method is used to update user by id

        :param uow: unit of work instance
        :param id: user id
        :param request: user view model
        :return: user
        """
        async with uow:
            if not await uow.user.find_one_or_none(id):
                raise NotFoundError(message="User not found")
            await uow.user.update_one(
                id, request.model_dump(exclude_unset=True)
            )

    @staticmethod
    async def delete_user(uow: AbstractUnitOfWork, id: int) -> None:
        """
        Delete user by id

        This method is used to delete user by id

        :param uow: unit of work instance
        :param id: user id
        """
        async with uow:
            if not await uow.user.find_one_or_none(id):
                raise NotFoundError(message="User not found")
            await uow.user.delete_one(id)
