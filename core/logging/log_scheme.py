from typing import Any, Optional

from pydantic import BaseModel


class LogsScheme(BaseModel):
    request: str
    request_headers: dict = {}
    request_body: Optional[Any] = None
    # ip_user: str
    user_id: int | None = None
    response_body: Optional[Any] = None
    time_response: float
