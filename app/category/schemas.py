from pydantic import BaseModel

from core.schemas.base import BaseORMSchema, BaseSchema


class CategoryBase(BaseModel):
    title: str
    status: bool | None = True
    parent_id: int | None = None


class CategoryBaseIDSchema(BaseModel):
    id: int


class CategoryBaseChildren(CategoryBase):
    children: CategoryBase | None = None


class CategoryResponse(
    BaseORMSchema, CategoryBaseIDSchema, CategoryBaseChildren
):
    pass


class CategoryCreate(BaseSchema):
    title: str
    status: bool | None = True
