from typing import Optional

from pydantic import BaseModel, Field


class TransactionIn(BaseModel):
    type: str = Field(alias="tipo")
    value: float = Field(alias="valor")

    account_number: int = Field(None, alias="numero_conta")
    source_account_id: Optional[int] = Field(None, alias="conta_id_origem")
    destination_account_id: Optional[int] = Field(None, alias="conta_id_destino")
    account_id: Optional[int] = Field(None, alias="conta_id")

    class Config:
        populate_by_name = True