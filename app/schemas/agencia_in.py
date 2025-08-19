from pydantic import BaseModel


class AgenciaIn(BaseModel):
    nome: str
    numero: str
    cidade: str
    estado: str