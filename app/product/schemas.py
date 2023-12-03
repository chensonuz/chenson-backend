from typing import List, Optional

from pydantic import BaseModel

from core.schemas.base import BaseORMSchema, BaseSchema, APIResponse


class ProductBase(BaseModel):
    title: str
    description: str
    price: int
    status: bool | None = False


class ProductBaseIDSchema(BaseModel):
    id: int


class ProductBaseCategoryIDSchema(BaseModel):
    category_id: int


class ProductResponse(
    BaseORMSchema, ProductBaseIDSchema, ProductBaseCategoryIDSchema, ProductBase
):
    pass


class ProductCreate(BaseSchema, ProductBaseCategoryIDSchema):
    title: str
    description: str
    price: int
    status: bool | None = False


class APIProductListResponse(APIResponse):
    data: List[ProductResponse] = None


class APIProductResponse(APIResponse):
    data: Optional[ProductResponse] = None
