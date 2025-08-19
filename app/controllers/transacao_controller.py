from fastapi import APIRouter, status, Depends, HTTPException

from app.dependencias.dependencias import fabrica_transacao_service
from app.schemas.transacao_in import TransacaoIn
from app.services.transacao_service import TransacaoService
from app.views.transacao_out import TransacaoOut, TransacaoHistoricoOut

router = APIRouter(prefix="/transacoes")



@router.get("/historico", status_code=status.HTTP_200_OK, response_model=list[TransacaoHistoricoOut])
async def historico(
        data = None,
        conta_id: int = None,
        numero_conta: int = None,
        limit: int = 100,
        skip: int = 0,
        service: TransacaoService = Depends(fabrica_transacao_service),
):
    return await service.get_historico(data=data, conta_id=conta_id, numero_conta=numero_conta, limit=limit, skip=skip)

@router.post("/depositar", status_code=status.HTTP_201_CREATED, response_model=TransacaoOut)
async def depositar(
        post: TransacaoIn,
        service: TransacaoService = Depends(fabrica_transacao_service),
):
    return await service.create_transacao(post)