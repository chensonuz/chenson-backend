from app.address.models import AddressInfo
from app.address.schemas import AddressCreateRequest, AddressResponse
from core.exceptions.classes import ConflictError, NotFoundError, ForbiddenError
from core.services.uow import AbstractUnitOfWork


class AddressService:
    """
    AddressService

    This class is responsible for handling all the business logic of the address module.
    """

    @staticmethod
    async def create(
        uow: AbstractUnitOfWork, data: AddressCreateRequest, user_id: int
    ) -> int:
        """
        Create address

        :param user_id: current user id
        :param uow: unit of work instance
        :param data: address data
        :return: created address
        """
        async with uow:
            if await uow.address_info.find_one_or_none_by(
                uow.address_info.model.address, data.address
            ) or await uow.address_info.find_one_or_none_by(
                uow.address_info.model.location, data.location
            ):
                raise ConflictError(f"Address {data.address} already exists")
            return await uow.address_info.add_one(
                data.to_orm(user_id=user_id).model_dump()
            )

    @staticmethod
    async def delete(uow: AbstractUnitOfWork, id: int, user_id: int) -> int:
        """
        Delete address

        :param user_id: current user id
        :param uow: unit of work instance
        :param id: address id
        :return: deleted address id
        """
        async with uow:
            address = await uow.address_info.find_one_or_none(id=id)
            if not address:
                raise NotFoundError(f"Address with id {id} not found")
            if address.user_id != user_id:
                raise ForbiddenError(
                    f"Address with id {id} doesn't belong to you"
                )
            return await uow.address_info.delete_one(id)

    @staticmethod
    async def get(
        uow: AbstractUnitOfWork, id: int, user_id: int
    ) -> AddressResponse:
        """
        Get address

        :param user_id: current user id
        :param uow: unit of work instance
        :param id: address id
        :return: address
        """
        async with uow:
            address: AddressInfo = await uow.address_info.find_one_or_none(
                id=id
            )
            if not address or address.user_id != user_id:
                raise NotFoundError(f"Address with id {id} not found")
            return AddressResponse.model_validate(address)

    @staticmethod
    async def get_all(
        uow: AbstractUnitOfWork, user_id: int
    ) -> list[AddressResponse]:
        """
        Get all addresses

        :param uow: unit of work instance
        :param user_id: current user id
        :return: addresses
        """
        async with uow:
            addresses: list[
                AddressInfo
            ] = await uow.address_info.find_all_by_filter(
                filters=[uow.address_info.model.user_id == user_id]
            )
            return [
                AddressResponse.model_validate(address) for address in addresses
            ]
