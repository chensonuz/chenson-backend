import pytest
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health(app: FastAPI, client: AsyncClient):
    response = await client.get(app.url_path_for("main:health"))
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
