from app.category.repository import CategoryRepository
from app.product.repository import ProductRepository
from app.user.repository import UserRepository
from core.database.db import async_session
from core.services.uow import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    """
    Unit of work pattern implementation
    """

    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user: UserRepository = UserRepository(self.session)
        self.category: CategoryRepository = CategoryRepository(self.session)
        self.product: ProductRepository = ProductRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
