from fastapi_filter.contrib.sqlalchemy import Filter

from app.product.models import Product


class ProductFilter(Filter):
    order_by: list[str] = ["-category_id"]
    category_id: int | None = None
    category_id__in: list[int] | None = None

    class Constants(Filter.Constants):
        model = Product
