from app.user.admin.auth import create_access_token, create_refresh_token
from app.user.admin.models import AdminUser
from app.user.admin.schemas import AdminLogInResponse
from app.user.utils import verify_password
from core.exceptions.classes import ForbiddenError
from core.services.uow import AbstractUnitOfWork


class AdminUserService:
    """
    Admin User service

    This service is responsible for admin-user-related operations

    List of responsibilities:
    - authenticate admin user
    """

    @staticmethod
    async def authenticate_admin(
        uow: AbstractUnitOfWork, email: str, password: str
    ) -> AdminLogInResponse:
        """
        Authenticate admin user

        This method is used to authenticate admin user by email and password.
        If user doesn't exist, None is returned.

        :param uow: unit of work instance
        :param email: email as string
        :param password: password as string
        :return: admin user view model
        """
        async with uow:
            admin_user: AdminUser = (
                await uow.admin_user.find_one_or_none_by_email(email)
            )
            if not admin_user:
                raise ForbiddenError(message="Incorrect email or password")

            if not verify_password(password, admin_user.password):
                raise ForbiddenError(message="Incorrect email or password")

            access_token = create_access_token(admin_user)
            refresh_token = create_refresh_token(admin_user)

            return AdminLogInResponse(
                access_token=access_token, refresh_token=refresh_token
            )
