import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from tests.utils import generate_init_data


@pytest.mark.anyio
async def test_auth_ok(app: FastAPI, client: AsyncClient):
    user_data, token = generate_init_data()
    headers = {"Authorization": token}
    response = await client.post(app.url_path_for("user:auth"), headers=headers)
    assert response.status_code == 200
    assert {
        "success": True,
        "message": "User authenticated",
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_auth_unauthorized(app: FastAPI, client: AsyncClient):
    headers = {"Authorization": "false"}
    response = await client.post(app.url_path_for("user:auth"), headers=headers)
    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "message": "Not authorized",
        "data": None,
    }
