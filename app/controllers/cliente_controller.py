from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencias.dependencias import fabrica_cliente_service
from app.schemas.cliente_in import ClienteIn
from app.services.cliente_service import ClienteService
from app.views.cliente_com_conta_out import ClienteComContaOut

router = APIRouter(prefix="/clientes")



@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ClienteComContaOut])
async def get_clientes(
        limit: int = 100,
        skip: int = 0,
        service: ClienteService = Depends(fabrica_cliente_service)
):
    return await service.get_clientes(limit=limit, skip=skip)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClienteComContaOut)
async def create_cliente(
        post: ClienteIn,
        service: ClienteService = Depends(fabrica_cliente_service)
):
    try:
        return await service.criar_cliente(post)
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este CPF já possui uma conta.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))