from pydantic import BaseModel


class AdminProductCreateRequest(BaseModel):
    name: str
    price: float
    description: str


class AdminProductUpdateRequest(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None
