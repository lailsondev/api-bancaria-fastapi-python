from pydantic import BaseModel, Field


class BranchOut(BaseModel):
    id: int
    name: str = Field(alias="nome")
    number: str = Field(alias="numero")
    city: str = Field(alias="cidade")
    state: str = Field(alias="estado")

    model_config = {
        "populate_by_name": True
    }