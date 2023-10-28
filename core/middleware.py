from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from core.config import AppConfig
from core.logging.logging import create_logs


async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        time_for_request = datetime.utcnow()

        await set_body(request, await request.body())
        body = await get_body(request)
        body_request = jsonable_encoder(body)

        response = await call_next(request)

        dict_logs = await create_logs(
            request=request,
            response=response,
            body_request=body_request,
            time_request=time_for_request,
        )
        logger.info(f"{dict_logs}")

        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=AppConfig.ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=["*"],
    )
