from pydantic import BaseModel


class AdminProductCreateRequest(BaseModel):
    category_id: int
    title: str
    description: str
    price: int
    status: bool | None = False


class AdminProductUpdateRequest(BaseModel):
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    status: bool | None = None
