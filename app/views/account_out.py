from datetime import datetime

from pydantic import BaseModel, Field


class AccountOut(BaseModel):
    id: int
    number: int = Field(alias="numero")
    balance: float = Field(alias="saldo")
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {
        "populate_by_name": True
    }