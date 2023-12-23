from abc import ABC, abstractmethod

from app.admin.repository import AdminUserRepository
from app.category.repository import CategoryRepository
from app.product.repository import ProductRepository, ProductImageRepository
from app.user.repository import UserRepository


class AbstractUnitOfWork(ABC):
    admin_user: AdminUserRepository
    user: UserRepository
    category: CategoryRepository
    product: ProductRepository
    product_image: ProductImageRepository

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
