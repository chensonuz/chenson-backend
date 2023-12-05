from app.admin.auth import create_access_token, create_refresh_token
from app.admin.schemas import (
    AdminLogInResponse,
    AdminUserBaseSchema,
)
from app.dependencies import UnitOfWorkDep
from app.user.utils import verify_password
from core.exceptions.classes import ForbiddenError


class AdminService:
    """Admin service.

    This service is responsible for admin-related operations.

    List of responsibilities:
    - authenticate admin user
    """

    @staticmethod
    async def authenticate_admin(uow: UnitOfWorkDep, email: str, password: str):
        """Authenticate admin user.

        This method is used to authenticate admin user by email and password.
        If user doesn't exist, None is returned.

        :param uow: unit of work instance
        :param email: email as string
        :param password: password as string
        :return: admin user view model
        """
        async with uow:
            admin_user = await uow.admin_user.find_one_or_none_by_email(email)
            if not admin_user:
                raise ForbiddenError(message="Incorrect email or password")

            if not verify_password(password, admin_user.password):
                raise ForbiddenError(message="Incorrect email or password")

            mapped_admin_user = AdminUserBaseSchema.model_validate(admin_user)

            access_token = create_access_token(
                mapped_admin_user.model_dump(mode="json")
            )
            refresh_token = create_refresh_token(
                mapped_admin_user.model_dump(mode="json")
            )

            return AdminLogInResponse(
                access_token=access_token, refresh_token=refresh_token
            )
