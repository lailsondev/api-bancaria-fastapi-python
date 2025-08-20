from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies.dependencies import factory_customer_service
from app.schemas.customer_in import CustomerIn
from app.services.customer_service import CustomerService
from app.views.customer_with_account_out import CustomerWithAccountOut

router = APIRouter(prefix="/clientes")



@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CustomerWithAccountOut])
async def get_customers(
        limit: int = 100,
        skip: int = 0,
        service: CustomerService = Depends(factory_customer_service)
):
    return await service.get_customers(limit=limit, skip=skip)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CustomerWithAccountOut)
async def get_custumer(
        id: int,
        service: CustomerService = Depends(factory_customer_service)
):
    return await service.get_custumer(id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CustomerWithAccountOut)
async def create_customer(
        post: CustomerIn,
        service: CustomerService = Depends(factory_customer_service)
):
    try:
        return await service.create_customer(post)
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este CPF já possui uma conta.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))