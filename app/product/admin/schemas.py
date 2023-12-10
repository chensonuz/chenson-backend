from pydantic import BaseModel


class AdminProductCreateRequest(BaseModel):
    category_id: int
    title: str
    description: str
    price: int
    status: bool | None = False


class AdminProductUpdateRequest(BaseModel):
    category_id: int
    title: str
    description: str
    price: int
    status: bool | None = False
