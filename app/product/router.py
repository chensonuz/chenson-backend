from fastapi import APIRouter, Depends

from app.dependencies import auth_service, UnitOfWorkDep
from app.product.schemas import (
    APIProductResponse,
    APIProductListResponse,
)
from app.product.service import ProductService

router = APIRouter(dependencies=[Depends(auth_service)])


@router.get("/all/{category_id}", response_model=APIProductListResponse)
async def get_products_by_category_id(
    category_id: int, uow: UnitOfWorkDep
) -> APIProductListResponse:
    return APIProductListResponse(
        success=True,
        message="Products by category retrieved.",
        data=await ProductService.get_products(uow, category_id),
    )


@router.get("/{id}", response_model=APIProductResponse)
async def get_product(
    category_id: int, uow: UnitOfWorkDep
) -> APIProductResponse:
    return APIProductResponse(
        success=True,
        message="Product retrieved",
        data=await ProductService.get_product(uow, category_id),
    )
