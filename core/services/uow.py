from abc import ABC, abstractmethod

from app.admin.repository import AdminUserRepository
from app.category.repository import CategoryRepository
from app.order.repository import OrderRepository, OrderItemRepository
from app.product.repository import ProductRepository, ProductImageRepository
from app.user.repository import UserRepository, AddressInfoRepository


class AbstractUnitOfWork(ABC):
    admin_user: AdminUserRepository
    user: UserRepository
    category: CategoryRepository
    product: ProductRepository
    product_image: ProductImageRepository
    order: OrderRepository
    order_item: OrderItemRepository
    address_info: AddressInfoRepository

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
