from fastapi import APIRouter

from app.dependencies import UnitOfWorkDep
from app.user.admin.schemas import AdminLogInRequest, AdminLogInResponse
from app.user.admin.service import AdminUserService

router = APIRouter()


@router.post("/auth", response_model=AdminLogInResponse)
async def authenticate_admin(request: AdminLogInRequest, uow: UnitOfWorkDep):
    return await AdminUserService.authenticate_admin(
        uow=uow, email=request.email, password=request.password
    )
