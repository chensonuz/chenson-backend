from app.uow import AbstractUnitOfWork
from app.user.database.models import User
from app.user.schemas.user import UserResponse, UserCreate


class UserService:
    """
    User service

    This service is responsible for user-related operations

    List of responsibilities:
    - register user
    - get users
    - get user
    - update user (as per database schema)
    - update user profile (only for name and schedule)
    """

    @staticmethod
    async def get_user(
        uow: AbstractUnitOfWork, telegram_id: int
    ) -> UserResponse | None:
        """
        Get user

        This method is used to get a user from the database by id. If user
        doesn't exist, None is returned.

        :param uow: unit of work instance
        :param telegram_id: telegram id as integer
        :return: user view model
        """
        async with uow:
            user: User = await uow.user.find_one_or_none_by_telegram_id(
                telegram_id
            )
            if user:
                return UserResponse.model_validate(user)

    @staticmethod
    async def register_user(uow: AbstractUnitOfWork, user: UserCreate) -> int:
        """
        Register user

        This method is used to register user in the database. It creates a
        schedule for the user with default values.

        :param uow: unit of work instance
        :param user: user view model
        :return: user id
        """
        async with uow:
            user_id = await uow.user.add_one(user.model_dump(exclude_none=True))
            await uow.commit()
            return user_id
