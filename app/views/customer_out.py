from datetime import date

from pydantic import BaseModel, Field


class CustomerOut(BaseModel):
    id: int
    name: str = Field(alias="nome")
    lastname: str = Field(alias="sobrenome")
    birth_date: date = Field(alias="data_nascimento")
    cpf: str

    model_config = {
        "populate_by_name": True
    }
