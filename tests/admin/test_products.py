import pytest
from httpx import AsyncClient
from loguru import logger

from app.category.admin.schemas import AdminCategoryCreateRequest
from app.product.admin.schemas import (
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
)
from tests.utils import TestUnitOfWorkDep


def _product(cat_id: int):
    return {
        "category_id": cat_id,
        "title": "Product 1",
        "description": "Product 1 description",
        "price": 100,
        "status": True,
    }


class TestAdminProducts:
    base_url = "/api/v1/admin/products"

    @pytest.fixture(scope="session", autouse=True)
    async def populate_data(self, override_uow: TestUnitOfWorkDep) -> int:
        category = AdminCategoryCreateRequest(
            title="Category 1",
            status=True,
        )
        async with override_uow:
            if not await override_uow.category.find_one_or_none_by_title(
                category.title
            ):
                return await override_uow.category.add_one(
                    category.model_dump()
                )

    @pytest.mark.anyio
    async def test_add_product(self, admin_client: AsyncClient):
        obj = AdminProductCreateRequest(**_product(2))
        response = await admin_client.post(self.base_url, json=obj.model_dump())
        response_data = response.json()
        logger.info(response_data)
        assert response.status_code == 201
        assert response_data["success"] is True
        assert response_data["message"] == "Product created."
        assert response_data["data"] == {"id": 1}

    @pytest.mark.anyio
    async def test_get_product(self, admin_client: AsyncClient):
        response = await admin_client.get(f"{self.base_url}/1")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Product retrieved."

        target_obj = _product(response_data["data"]["category_id"])
        assert response_data["data"]["id"] == 1
        assert response_data["data"]["status"] is target_obj["status"]
        assert response_data["data"]["title"] == target_obj["title"]
        assert response_data["data"]["description"] == target_obj["description"]
        assert response_data["data"]["price"] == target_obj["price"]

    @pytest.mark.anyio
    async def test_patch_product(self, admin_client: AsyncClient):
        obj = AdminProductUpdateRequest(status=False, title="Product 2")
        response = await admin_client.patch(
            f"{self.base_url}/1", json=obj.model_dump(exclude_unset=True)
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Product updated."
        assert response_data["data"]["id"] == 1

        response = await admin_client.get(f"{self.base_url}/1")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["data"]["status"] is False
        assert response_data["data"]["title"] == "Product 2"

    @pytest.mark.anyio
    async def test_get_products(self, admin_client: AsyncClient):
        response = await admin_client.get(self.base_url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Products retrieved."
        assert len(response_data["data"]) > 0

    @pytest.mark.anyio
    async def test_delete_product(self, admin_client: AsyncClient):
        response = await admin_client.delete(f"{self.base_url}/1")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Product deleted."
        assert response_data["data"]["id"] == 1

        response = await admin_client.get(f"{self.base_url}/1")
        assert response.status_code == 404
