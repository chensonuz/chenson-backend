from app.address.models import AddressInfo
from core.repositories.base import SQLAlchemyRepository


class AddressInfoRepository(SQLAlchemyRepository):
    model = AddressInfo
