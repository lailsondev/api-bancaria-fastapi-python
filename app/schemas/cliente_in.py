from datetime import date, datetime

from pydantic import BaseModel, field_validator


class ClienteIn(BaseModel):
    nome: str
    sobrenome: str
    data_nascimento: date
    cpf: str
    agencia_id: int

    @field_validator('data_nascimento', mode='before')
    @classmethod
    def parse_data_nascimento(cls, value):
        try:
            dt_object = datetime.strptime(value, '%d/%m/%Y')

            return dt_object.date()
        except ValueError:
            raise ValueError("Formato de data inválido. Use 'DD/MM/YYYY'")
