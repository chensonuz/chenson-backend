from fastapi import APIRouter, Depends

from app.category.schemas import APICategoryListResponse
from app.category.service import CategoryService
from app.dependencies import auth_service, UnitOfWorkDep

router = APIRouter(dependencies=[Depends(auth_service)])


@router.get("", response_model=APICategoryListResponse)
async def get_categories(
    uow: UnitOfWorkDep,
) -> APICategoryListResponse:
    return APICategoryListResponse(
        success=True,
        message="Categories retrieved.",
        data=await CategoryService.get_categories(uow),
    )
