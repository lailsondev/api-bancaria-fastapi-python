from fastapi import Depends, status, APIRouter

from app.dependencias.dependencies import factory_branch_service
from app.schemas.branch_in import BranchIn
from app.services.branch_service import BranchService
from app.views.branch_out import BranchOut

router = APIRouter(prefix="/agencias")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[BranchOut])
async def get_branchs(
        limit: int = 100,
        skip: int = 0,
        service: BranchService = Depends(factory_branch_service)
):
    return await service.get_all(limit=limit, skip=skip)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BranchOut)
async def get_branch(
        id: int,
        service: BranchService = Depends(factory_branch_service)
):
    return await service.get(id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BranchOut)
async def create_branch(
        post: BranchIn,
        service: BranchService = Depends(factory_branch_service)
):
    return await service.create(post)