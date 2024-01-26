from fastapi import APIRouter, Depends

from app.address.schemas import (
    AddressCreateRequest,
    APIAddressResponse,
    APIAddressListResponse,
)
from app.address.service import AddressService
from app.dependencies import UnitOfWorkDep, get_current_user
from app.user.schemas import UserResponse
from core.schemas.base import APIResponseWithID, APIResponseID

router = APIRouter()


@router.post(
    "", name="address:create", status_code=201, response_model=APIResponseWithID
)
async def address_create(
    uow: UnitOfWorkDep,
    data: AddressCreateRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """Create address"""
    created_id = await AddressService.create(
        uow=uow, data=data, user_id=current_user.id
    )
    return APIResponseWithID(
        success=True,
        message="Address created.",
        data=APIResponseID(id=created_id),
    )


@router.get(
    "/{address_id}", name="address:get", response_model=APIAddressResponse
)
async def address_get(
    address_id: int,
    uow: UnitOfWorkDep,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get address"""
    return APIAddressResponse(
        success=True,
        message="Address retrieved.",
        data=await AddressService.get(uow=uow, id=address_id),
    )


@router.get("", name="address:get_all", response_model=APIAddressListResponse)
async def address_get_all(
    uow: UnitOfWorkDep,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get all addresses"""
    return APIAddressListResponse(
        success=True,
        message="Addresses retrieved.",
        data=await AddressService.get_all(uow=uow, user_id=current_user.id),
    )


@router.delete(
    "/{address_id}", name="address:delete", response_model=APIResponseWithID
)
async def address_delete(
    address_id: int,
    uow: UnitOfWorkDep,
    current_user: UserResponse = Depends(get_current_user),
):
    """Delete address"""
    deleted_id = await AddressService.delete(
        uow=uow, id=address_id, user_id=current_user.id
    )
    return APIResponseWithID(
        success=True,
        message="Address deleted.",
        data=APIResponseID(id=deleted_id),
    )
