from app.product.models import Product
from app.product.schemas import ProductImageSchema, ProductResponse


def db_to_domain(data: Product) -> ProductResponse:
    images = [ProductImageSchema.model_validate(image) for image in data.images]
    return ProductResponse(
        id=data.id,
        category_id=data.category_id,
        title=data.title,
        description=data.description,
        price=data.price,
        status=data.status,
        images=images,
        created_at=data.created_at,
        updated_at=data.updated_at,
    )
