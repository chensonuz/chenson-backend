from abc import ABC, abstractmethod

from app.category.repository import CategoryRepository
from app.product.repository import ProductRepository
from app.user.repository import UserRepository


class AbstractUnitOfWork(ABC):
    user: UserRepository
    category: CategoryRepository
    product: ProductRepository

    @abstractmethod
    def __init__(self, *args):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...
