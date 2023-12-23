from pydantic import BaseModel, model_validator
from pydantic import field_validator

from app.utils.images import is_valid_media_path
from core.config import PRODUCT_IMAGES_DIR


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
    id: int | None = None
    image: str

    to_be_deleted: bool
    to_be_created: bool

    @model_validator(mode="after")
    def validate_model(self) -> "AdminProductImageUpdateRequest":
        is_valid_media_path(self.image)

        if ";base64," in self.image:
            if not self.to_be_created:
                raise ValueError(
                    "Image must be created if base64 encoded sent."
                )
            if self.to_be_deleted:
                raise ValueError(
                    "Can't delete and create image at the same time."
                )
            self.id = None
        elif f"{PRODUCT_IMAGES_DIR}/" in self.image:
            if self.to_be_created:
                raise ValueError(
                    "Image must be base64 encoded if created sent."
                )
            if self.to_be_deleted:
                if not self.id:
                    raise ValueError("Can't delete image without id.")
        else:
            raise ValueError("Incorrect image path.")
        return self


class AdminProductUpdateRequest(BaseModel):
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    status: bool | None = None
    images: list[AdminProductImageUpdateRequest] | None = None
