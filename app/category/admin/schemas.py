from pydantic import BaseModel


class AdminCategoryCreateRequest(BaseModel):
    title: str
    status: bool | None = True
    parent_id: int | None = None


class AdminCategoryUpdateRequest(BaseModel):
    title: str | None = None
    status: bool | None = None
    parent_id: int | None = None


class AdminCategoryUpdatePartialRequest(BaseModel):
    title: str | None = None
    status: bool | None = None
    parent_id: int | None = None


class AdminCategoryDeleteRequest(BaseModel):
    id: int
