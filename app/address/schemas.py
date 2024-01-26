from pydantic import BaseModel

from core.schemas.base import BaseORMSchema, BaseSchema, APIResponse


class AddressBaseUserID(BaseModel):
    """Address base user id"""

    user_id: int


class AddressBase(BaseModel):
    """Address base"""

    address: str
    location: str
    apartment: str | None = None
    comment: str | None = None
    entrance: str | None = None
    floor: str | None = None


class AddressBaseID(BaseModel):
    """Address base id"""

    id: int


class AddressResponse(
    BaseORMSchema, AddressBaseID, AddressBaseUserID, AddressBase
):
    """Address response"""

    ...


class AddressCreate(AddressBaseUserID, AddressBase, BaseSchema):
    """Address create for db"""

    ...


class AddressCreateRequest(AddressBase):
    """Address create request"""

    def to_orm(self, user_id: int) -> AddressCreate:
        """Convert to orm"""
        return AddressCreate(**self.model_dump(), user_id=user_id)


class APIAddressResponse(APIResponse):
    """API response list addresses"""

    data: AddressResponse = None


class APIAddressListResponse(APIResponse):
    """API response list addresses"""

    data: list[AddressResponse] = None
