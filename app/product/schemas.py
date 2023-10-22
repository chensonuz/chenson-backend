from pydantic import BaseModel

from core.schemas.base import BaseORMSchema, BaseSchema


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
    BaseORMSchema, ProductBaseIDSchema, ProductBaseCategoryIDSchema
):
    pass


class ProductCreate(BaseSchema, ProductBaseCategoryIDSchema):
    title: str
    description: str
    price: int
    status: bool | None = False
