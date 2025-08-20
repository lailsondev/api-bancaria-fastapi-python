from pydantic import BaseModel, Field


class BranchIn(BaseModel):
    name: str = Field(alias="nome")
    number: str = Field(alias="numero")
    city: str = Field(alias="cidade")
    state: str = Field(alias="estado")

    class Config:
        populate_by_name = True