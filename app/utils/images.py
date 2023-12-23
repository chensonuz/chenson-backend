import base64
import io
import os
from datetime import datetime
from random import randint

from PIL import Image
from loguru import logger

from core.config import MEDIA_DIR, PRODUCT_IMAGES_DIR
from core.exceptions.classes import ValuePydanticError


def get_random_filename():
    return f"{int(datetime.now().microsecond) * randint(10**6, 10**8-1)}_{datetime.now().date()}"


def decoder_image(image_base64: str):
    format_image, code_image = image_base64.split(";base64,")
    image = Image.open(
        io.BytesIO(base64.decodebytes(bytes(code_image, "utf-8")))
    )
    format_image = format_image.split("/")[-1]

    if format_image != "jpeg":
        image = image.convert("RGBA")

    return image, format_image


def is_valid_base64_or_none(img: str | None) -> bool:
    if not img or ";base64," in img:
        return True
    raise ValuePydanticError(message="Incorrect base64 image format.")


def is_valid_media_path(field: str | None) -> bool:
    if not field or (";base64," in field or f"{MEDIA_DIR}/" in field):
        return True
    raise ValuePydanticError(message="Incorrect media path.")


def save_image(image: str | None, fp: str) -> str | None:
    if not image or ";base64," not in image:
        return None

    parent_folder = os.path.dirname(fp)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    try:
        decoded_image, format_image = decoder_image(image)
        fp = f"{fp}{format_image}".replace("//", "/")
        decoded_image.save(fp)
        return fp
    except Exception as e:
        logger.info(e)
        return None


def delete_file(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


async def async_save_image(image: str | None, fp: str) -> str | None:
    return save_image(image, fp)


def filter_product_images(images: list[str]) -> (list[str], list[str]):
    to_be_created = []
    existing = []
    for image in images:
        if ";base64," in image:
            to_be_created.append(image)
        else:
            existing.append(image)
    return existing, to_be_created


def create_product_images(images: list[str], product_id: int) -> list[dict]:
    if not images:
        return []
    images_fps = [
        save_image(
            image,
            f"{PRODUCT_IMAGES_DIR}/{get_random_filename()}_{product_id}.",
        )
        for image in images[:3]
    ]
    return [
        {"product_id": product_id, "image": img_url} for img_url in images_fps
    ]
