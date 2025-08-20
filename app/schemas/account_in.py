from pydantic import BaseModel

class AccountIn(BaseModel):
    number: int
    balance: float
    customer_id: int
    branch_id: int

    class Config:
        populate_by_name = True


class UniqueAccountIn(BaseModel):
    id: int | None = None
    number: int | None = None
    destination_account_id: int | None = None
    type: str | None = None

    class Config:
        populate_by_name = True