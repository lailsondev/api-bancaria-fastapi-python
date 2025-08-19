from datetime import date

from pydantic import BaseModel

from app.views.conta_out import ContaOut


class ClienteComContaOut(BaseModel):
    id: int
    nome: str
    sobrenome: str
    data_nascimento: date
    cpf: str

    conta: ContaOut