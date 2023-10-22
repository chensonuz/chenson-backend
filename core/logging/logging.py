import json
from datetime import datetime

import jwt
from fastapi import Request, Response
from starlette.concurrency import iterate_in_threadpool

from core.config import AppConfig
from core.logging.log_scheme import LogsScheme


def get_user_id(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", None)

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    try:
        token_data = jwt.decode(
            token,
            AppConfig.ACCESS_SECRET_KEY,
            algorithms=[AppConfig.JWT_ALGORITHM],
        )
        return token_data.get("id", None)
    except:
        return None


def get_app_version(request: Request) -> str | None:
    return request.headers.get("App-Version", None)


async def create_logs(
    request: Request,
    response: Response,
    body_request: str,
    time_request: datetime,
):
    response_body_logs = None

    body_request_log = "..."

    if body_request and len(body_request) <= 4096:
        try:
            body_request_log = json.loads(body_request)
        except:
            body_request_log = "INVALID"

    if int(response.status_code) >= 400:
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        if len(response_body) > 0:
            response_body_logs = response_body[0].decode()

    user_id = get_user_id(request=request)

    logs = LogsScheme(
        request=f"{time_request} - {request.method} - {request.url} - {response.status_code}",
        request_headers={
            k.decode(): v.decode() for k, v in request.headers.raw
        },
        request_body=body_request_log,
        # ip_user=request.user.host,
        # user_id=user_id,
        response_body=response_body_logs,
        time_response=(datetime.utcnow() - time_request).total_seconds(),
    )

    return logs
