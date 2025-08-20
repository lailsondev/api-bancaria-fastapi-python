import datetime as dt

from pydantic import BaseModel, field_validator, Field


class CustomerIn(BaseModel):
    name: str = Field(alias="nome")
    lastname: str = Field(alias="sobrenome")
    birth_date: dt.date = Field(alias="data_nascimento")
    cpf: str
    branch_id: int = Field(alias="agencia_id")

    @field_validator('birth_date', mode='before')
    @classmethod
    def parse_birth_date(cls, value):
        try:
            dt_object = dt.datetime.strptime(value, '%d/%m/%Y')

            return dt_object.date()
        except ValueError:
            raise ValueError("Formato de data inválido. Use 'DD/MM/YYYY'")


    class Config:
        populate_by_name = True
