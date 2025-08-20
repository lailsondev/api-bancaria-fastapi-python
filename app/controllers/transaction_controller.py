from fastapi import APIRouter, status, Depends

from app.schemas.auth_in import LoginIn
from app.security import login_required

from app.dependencias.dependencies import factory_transaction_service
from app.schemas.transaction_in import TransactionIn
from app.services.transaction_service import TransactionService
from app.views.transaction_out import TransactionOut, TransactionHistoryOut

router = APIRouter(prefix="/transacoes", dependencies=[Depends(login_required)])



@router.get("/historico", status_code=status.HTTP_200_OK, response_model=list[TransactionHistoryOut])
async def get_histories(
        data = None,
        conta_id: int = None,
        numero_conta: int = None,
        limit: int = 100,
        skip: int = 0,
        service: TransactionService = Depends(factory_transaction_service),
):
    return await service.get_history(date=data, account_id=conta_id, account_number=numero_conta, limit=limit, skip=skip)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransactionOut)
async def perform_transfer(
        post: TransactionIn,
        service: TransactionService = Depends(factory_transaction_service),
):
    return await service.create_transaction(post)