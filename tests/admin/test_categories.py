import pytest
from httpx import AsyncClient

from app.category.admin.schemas import (
    AdminCategoryCreateRequest,
    AdminCategoryUpdateRequest,
)


class TestAdminCategories:
    auth_url = "/api/v1/admin/auth"
    base_url = "/api/v1/admin/categories"
    category = {
        "title": "Category 1",
        "status": True,
    }

    @pytest.mark.anyio
    async def test_add_category(self, admin_client: AsyncClient):
        obj = AdminCategoryCreateRequest(
            title=self.category["title"], status=self.category["status"]
        )
        response = await admin_client.post(self.base_url, json=obj.model_dump())
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["success"] is True
        assert response_data["message"] == "Category created."
        assert response_data["data"] == {"id": 1}

    @pytest.mark.anyio
    async def test_get_category(self, admin_client: AsyncClient):
        response = await admin_client.get(f"{self.base_url}/1")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Category retrieved."
        assert response_data["data"]["id"] == 1
        assert response_data["data"]["status"] is self.category["status"]
        assert response_data["data"]["title"] == self.category["title"]

    @pytest.mark.anyio
    async def test_patch_category(self, admin_client: AsyncClient):
        obj = AdminCategoryUpdateRequest(status=False, title="Category 2")
        response = await admin_client.patch(
            f"{self.base_url}/1", json=obj.model_dump(exclude_unset=True)
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Category updated."
        assert response_data["data"]["id"] == 1

        response = await admin_client.get(f"{self.base_url}/1")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["data"]["status"] is False
        assert response_data["data"]["title"] == "Category 2"

    @pytest.mark.anyio
    async def test_get_categories(self, admin_client: AsyncClient):
        response = await admin_client.get(self.base_url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Categories retrieved."
        assert len(response_data["data"]) > 0

    @pytest.mark.anyio
    async def test_delete_category(self, admin_client: AsyncClient):
        response = await admin_client.delete(f"{self.base_url}/1")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "Category deleted."
        assert response_data["data"]["id"] == 1

        response = await admin_client.get(f"{self.base_url}/1")
        assert response.status_code == 404
