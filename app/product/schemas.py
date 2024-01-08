from typing import List, Optional

from pydantic import BaseModel
from pydantic import field_validator

from app.category.schemas import CategoryResponse
from app.utils.images import is_valid_media_path
from core.schemas.base import BaseORMSchema, APIResponse


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    status: bool | None = False


class ProductBaseIDSchema(BaseModel):
    id: int


class ProductBaseCategoryIDSchema(BaseModel):
    category_id: int


class ProductImageSchema(BaseORMSchema):
    id: int
    product_id: int
    image: str

    @field_validator("image")
    def validate_image(cls, v: str | None) -> str | None:
        if is_valid_media_path(v):
            return v


class ProductImagesSchema(BaseModel):
    images: list[ProductImageSchema] = None


class ProductResponse(
    BaseORMSchema,
    ProductBaseIDSchema,
    ProductBaseCategoryIDSchema,
    ProductBase,
    ProductImagesSchema,
):
    category: Optional[CategoryResponse] = None


class OrderProductResponse(
    BaseORMSchema, ProductBaseIDSchema, ProductBaseCategoryIDSchema
):
    title: str
    price: float


class APIProductListResponse(APIResponse):
    data: List[ProductResponse] = None


class APIProductResponse(APIResponse):
    data: Optional[ProductResponse] = None
