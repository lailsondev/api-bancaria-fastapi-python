from datetime import date

from pydantic import BaseModel


class ClienteOut(BaseModel):
    id: int
    nome: str
    sobrenome: str
    data_nascimento: date
    cpf: str
