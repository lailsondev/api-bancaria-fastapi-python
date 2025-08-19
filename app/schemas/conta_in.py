from pydantic import BaseModel

class ContaIn(BaseModel):
    numero: int
    saldo: float
    cliente_id: int
    agencia_id: int


class ContaUnicaIn(BaseModel):
    id: int | None = None
    numero: int | None = None
    conta_id_destino: int | None = None
    tipo: str | None = None