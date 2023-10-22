from typing import List

from fastapi import APIRouter, Depends

from app.category.schemas import CategoryResponse
from app.category.service import CategoryService
from app.dependencies import auth_service, UnitOfWorkDep
from core.schemas.base import APIDetailedResponse

router = APIRouter(dependencies=[Depends(auth_service)])

APIListResponse = APIDetailedResponse(List[CategoryResponse])


@router.get("", response_model=APIListResponse)
async def get_categories(
    uow: UnitOfWorkDep,
) -> APIListResponse:
    return APIListResponse(
        success=True,
        message="Categories retrieved.",
        data=await CategoryService.get_categories(uow),
    )
