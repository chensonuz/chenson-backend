from typing import List

from fastapi import APIRouter, Depends

from app.product.schemas import ProductResponse
from app.product.service import ProductService
from app.dependencies import auth_service, UnitOfWorkDep
from core.schemas.base import APIDetailedResponse

router = APIRouter(dependencies=[Depends(auth_service)])

APIListResponse = APIDetailedResponse(List[ProductResponse])
APIResponse = APIDetailedResponse(ProductResponse)


@router.get("/all/{category_id}", response_model=APIListResponse)
async def get_products_by_category_id(
    category_id: int, uow: UnitOfWorkDep
) -> APIListResponse:
    return APIListResponse(
        status=True,
        message="Products by category retrieved.",
        data=await ProductService.get_products(uow, category_id),
    )


@router.get("/{id}", response_model=APIResponse)
async def get_product(category_id: int, uow: UnitOfWorkDep) -> APIResponse:
    return APIResponse(
        status=True,
        message="Product retrieved.",
        data=await ProductService.get_products(uow, category_id),
    )
