from pydantic import BaseModel, model_validator
from pydantic import field_validator

from app.utils.images import is_valid_media_path


class AdminProductCreateRequest(BaseModel):
    category_id: int
    title: str
    description: str
    price: int
    status: bool | None = False
    images: list[str] | None = None

    @field_validator("images")
    def validate_image(cls, vs: list[str] | None) -> list[str] | None:
        if all(is_valid_media_path(v) for v in vs):
            return vs


class AdminProductImageUpdateRequest(BaseModel):
    to_be_deleted: list[int] | None = None
    to_be_created: list[str] | None = None

    @model_validator(mode="after")
    def validate_model(self) -> "AdminProductImageUpdateRequest":
        for image in self.to_be_created or []:
            is_valid_media_path(image)

            if ";base64," not in image:
                raise ValueError("Incorrect base64 image format.")
        return self


class AdminProductUpdateRequest(BaseModel):
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    status: bool | None = None
    images: AdminProductImageUpdateRequest | None = None
