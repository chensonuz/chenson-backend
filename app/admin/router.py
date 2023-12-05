from fastapi import APIRouter, Depends

from app.admin.schemas import AdminLogInResponse, AdminLogInRequest
from app.admin.service import AdminService
from app.dependencies import UnitOfWorkDep

router = APIRouter()


@router.post("/auth", response_model=AdminLogInResponse)
async def admin_authenticate(request: AdminLogInRequest, uow: UnitOfWorkDep):
    return await AdminService.authenticate_admin(
        uow=uow, email=request.email, password=request.password
    )
