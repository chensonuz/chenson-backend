import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from loguru import logger

from app.user.schemas import TelegramUser
from tests.utils import generate_init_data


class TestSignInUp:
    url_name_auth = "user:auth"
    url_name_request_sms = "user:request_sms"

    user_data = TelegramUser(
        id=3392122312,
        first_name="Test23",
        last_name="Testov4",
        username="testtestov1",
        language_code="en",
        added_to_attachment_menu=True,
    )

    @pytest.fixture
    async def _token(self):
        yield generate_init_data(self.user_data)[1]

    @pytest.mark.anyio
    async def test_auth_new_user_ok(
        self, app: FastAPI, client: AsyncClient, _token: str
    ):
        response = await client.post(
            app.url_path_for(self.url_name_auth),
            headers={"Authorization": _token},
        )
        response_data = response.json()
        logger.warning(response_data)
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["data"]["created"] is True

    @pytest.mark.anyio
    async def test_auth_request_sms_ok(
        self, app: FastAPI, client: AsyncClient, _token: str
    ):
        phone_number = "+998900631455"
        response = await client.post(
            app.url_path_for(self.url_name_request_sms),
            headers={"Authorization": _token},
            json={"phone_number": phone_number},
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["message"] == "SMS code sent"

    @pytest.mark.anyio
    async def test_auth_existing_user_ok(
        self, app: FastAPI, client: AsyncClient
    ):
        _, token = generate_init_data(self.user_data)
        headers = {"Authorization": token}
        response = await client.post(
            app.url_path_for(self.url_name_auth), headers=headers
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["data"]["created"] is False

    @pytest.mark.anyio
    async def test_auth_unauthorized(self, app: FastAPI, client: AsyncClient):
        headers = {"Authorization": "false"}
        response = await client.post(
            app.url_path_for(self.url_name_auth), headers=headers
        )
        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "Not authorized",
            "data": None,
        }
