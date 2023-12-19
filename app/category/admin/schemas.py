from pydantic import BaseModel


class AdminCategoryCreateRequest(BaseModel):
    title: str
    status: bool | None = True


class AdminCategoryUpdateRequest(BaseModel):
    title: str | None = None
    status: bool | None = None


class AdminCategoryUpdatePartialRequest(BaseModel):
    title: str | None = None
    status: bool | None = None


class AdminCategoryDeleteRequest(BaseModel):
    id: int
