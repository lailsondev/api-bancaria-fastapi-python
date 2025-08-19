from pydantic import BaseModel


class LoginIn(BaseModel):
    cliente_id: int