import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field

from app.views.branch_out import BranchOut
from app.views.customer_out import CustomerOut
from app.views.account_out import AccountOut


class TransactionOut(BaseModel):
    id: int
    type: str = Field(alias="tipo")
    value: float = Field(alias="valor")
    account_number: int = Field(alias="numero_conta")
    date: dt.date = Field(alias="data")
    hour: dt.time = Field(alias="hora")
    created_at: Optional[dt.datetime] = Field(None, alias="nome")
    source_account_id: Optional[int] = Field(None, alias="conta_id_origem")
    destination_account_id: Optional[int] = Field(None, alias="conta_id_destino")
    account_id: Optional[int] = Field(None, alias="conta_id")

    account: AccountOut = Field(alias="conta")

    class Config:
        populate_by_name = True


class TransactionHistoryOut(BaseModel):
    id: int
    type: str = Field(alias="tipo")
    value: float = Field(alias="valor")
    account_number: int = Field(alias="numero_conta")
    date: dt.date = Field(alias="data")
    hour: dt.time = Field(alias="hora")
    created_at: Optional[dt.datetime] = Field(None, alias="nome")
    source_account_id: Optional[int] = Field(None, alias="conta_id_origem")
    destination_account_id: Optional[int] = Field(None, alias="conta_id_destino")
    account_id: Optional[int] = Field(None, alias="conta_id")

    account: AccountOut = Field(alias="conta")
    customer: CustomerOut = Field(alias="cliente")
    branch: BranchOut = Field(alias="agencia")

    model_config = {
        "populate_by_name": True
    }