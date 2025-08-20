from fastapi import Depends, status, APIRouter

from app.dependencias.dependencias import fabrica_agencia_service
from app.schemas.agencia_in import AgenciaIn
from app.services import agencia_service
from app.services.agencia_service import AgenciaService
from app.views.agencia_out import AgenciaOut

router = APIRouter(prefix="/agencias")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AgenciaOut])
async def get_agencias(
        limit: int = 100,
        skip: int = 0,
        service: AgenciaService = Depends(fabrica_agencia_service)
):
    return await service.get_all(limit=limit, skip=skip)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=AgenciaOut)
async def get_agencia(
        id: int,
        service: AgenciaService = Depends(fabrica_agencia_service)
):
    return await service.get(id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AgenciaOut)
async def create_agencia(
        post: AgenciaIn,
        service: AgenciaService = Depends(fabrica_agencia_service)
):
    return await service.create(post)