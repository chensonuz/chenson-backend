from typing import List

from pydantic import BaseModel

from core.schemas.base import BaseORMSchema, APIResponse


class CategoryBase(BaseModel):
    title: str
    status: bool | None = True


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


class APICategoryResponse(APIResponse):
    data: CategoryResponse = None


class APICategoryListResponse(APIResponse):
    data: List[CategoryResponse] = None
