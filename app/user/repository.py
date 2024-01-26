from app.user.models import User
from core.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_one_by_telegram_id(self, value, **kwargs):
        return await super().find_one_by(
            self.model.telegram_id, value, options=[]
        )

    async def find_one_or_none_by_telegram_id(self, value, **kwargs):
        return await super().find_one_or_none_by(
            self.model.telegram_id, value, options=[]
        )
