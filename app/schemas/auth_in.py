from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    customer_id: int = Field(alias="cliente_id")

    class Config:
        populate_by_name = True