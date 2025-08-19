from typing import Optional

from pydantic import BaseModel


class TransacaoIn(BaseModel):
    tipo: str
    valor: float
    numero_conta: int
    conta_id_origem: Optional[int] = None
    conta_id_destino: Optional[int] = None
    conta_id: Optional[int] = None