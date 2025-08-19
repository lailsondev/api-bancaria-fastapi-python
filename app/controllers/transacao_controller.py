from fastapi import APIRouter, status, Depends

from app.schemas.auth_in import LoginIn
from app.seguranca import login_required

from app.dependencias.dependencias import fabrica_transacao_service
from app.schemas.transacao_in import TransacaoIn
from app.services.transacao_service import TransacaoService
from app.views.transacao_out import TransacaoOut, TransacaoHistoricoOut

router = APIRouter(prefix="/transacoes", dependencies=[Depends(login_required)])



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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransacaoOut)
async def efetuar_transacao(
        post: TransacaoIn,
        service: TransacaoService = Depends(fabrica_transacao_service),
):
    return await service.create_transacao(post)