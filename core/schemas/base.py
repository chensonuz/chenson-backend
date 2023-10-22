from datetime import datetime
from typing import Type, Union

from pydantic import BaseModel, ConfigDict, create_model


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None


class _APIDetailedResponse:
    def __call__(
        self, data_type: Union[type, Type[BaseModel]]
    ) -> Type[BaseModel]:
        return create_model(
            "APIResponse",
            success=(bool, None),
            message=(str, None),
            data=(data_type | None, None),
        )


APIDetailedResponse = _APIDetailedResponse()


class BaseSchema(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BaseORMSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)
