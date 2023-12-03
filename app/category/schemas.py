from typing import List

from pydantic import BaseModel

from core.schemas.base import BaseORMSchema, BaseSchema, APIResponse


class CategoryBase(BaseModel):
    title: str
    status: bool | None = True
    parent_id: int | None = None


class CategoryBaseIDSchema(BaseModel):
    id: int


class CategoryBaseChildren(CategoryBase):
    children: CategoryBase | None = None


class CategoryResponseWithChildren(
    BaseORMSchema, CategoryBaseIDSchema, CategoryBaseChildren
):
    pass


class CategoryResponse(BaseORMSchema, CategoryBaseIDSchema, CategoryBase):
    pass


class CategoryCreate(BaseSchema):
    title: str
    status: bool | None = True


class APICategoryListResponse(APIResponse):
    data: List[CategoryResponse] = None
