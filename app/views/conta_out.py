from datetime import datetime

from pydantic import BaseModel


class ContaOut(BaseModel):
    id: int
    numero: int
    saldo: float
    created_at: datetime
    updated_at: datetime | None = None