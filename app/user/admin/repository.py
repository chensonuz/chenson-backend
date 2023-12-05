from app.user.admin.models import AdminUser
from core.repositories.base import SQLAlchemyRepository


class AdminUserRepository(SQLAlchemyRepository):
    model = AdminUser

    async def find_one_or_none_by_email(self, value, **kwargs):
        return await super().find_one_or_none_by(
            self.model.email, value, options=[]
        )
