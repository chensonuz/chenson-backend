from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from app.bot.dependencies import get_bot_instance
from app.user.models import User
from app.user.schemas import UserResponse, UserCreate
from core.config import MEDIA_DIR
from core.services.uow import AbstractUnitOfWork


class UserService:
    """
    User service

    This service is responsible for user-related operations

    List of responsibilities:
    - register user
    - get users
    - get user
    - update user (as per database schema)
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
                profile_photo = await UserService.get_user_profile_photos(
                    get_bot_instance(), user.telegram_id
                )
                if user.photo_url != profile_photo:
                    await uow.user.update_one(
                        user.id, {"photo_url": profile_photo}
                    )
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
            user.photo_url = await UserService.get_user_profile_photos(
                get_bot_instance(), user.telegram_id
            )
            user_id = await uow.user.add_one(user.model_dump(exclude_none=True))
            return user_id

    @staticmethod
    async def get_user_profile_photos(bot: Bot, id: int) -> str | None:
        """
        Get user profile photos

        This method is used to get user profile photos

        :param bot:
        :param id: user id
        :return: user profile photos
        """
        async with bot.session:
            try:
                result = await bot.get_user_profile_photos(id, limit=1)
            except TelegramBadRequest:
                return None

            if result.total_count < 1:
                return None

            fp = f"{MEDIA_DIR}/profile_photos/{id}.jpeg"
            await bot.download(result.photos[0][-1].file_id, fp)
            return fp
