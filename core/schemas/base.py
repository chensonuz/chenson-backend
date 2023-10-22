from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BaseORMSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None
