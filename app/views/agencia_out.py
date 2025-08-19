from pydantic import BaseModel


class AgenciaOut(BaseModel):
    id: int
    nome: str
    numero: str
    cidade: str
    estado: str