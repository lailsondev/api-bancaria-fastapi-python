from datetime import date

from pydantic import BaseModel, Field

from app.views.account_out import AccountOut


class CustomerWithAccountOut(BaseModel):
    id: int
    name: str = Field(alias="nome")
    lastname: str = Field(alias="sobrenome")
    birth_date: date = Field(alias="data_nascimento")
    cpf: str

    account: AccountOut = Field(alias="conta")

    class Config:
        populate_by_name = True