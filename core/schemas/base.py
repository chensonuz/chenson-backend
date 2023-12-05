from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None


class APIResponseID(BaseModel):
    id: int | str


class APIResponseWithID(APIResponse):
    data: APIResponseID = None


class BaseSchema(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BaseORMSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class EmptySchema(BaseModel):
    pass
