from typing import Optional

from databases.interfaces import Record

from app.repositories.account_repository import AccountRepository
from app.schemas.account_in import AccountIn
from app.views.account_out import AccountOut


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    async def create_account(self, post: AccountIn) -> AccountOut:
        return await self.repository.create_account(post)

    async def get_account(self, **kwargs) -> Optional[Record]:
        return await self.repository.get_account(**kwargs)

    async def update_balance(self, new_balance, account_id):
        return await self.repository.update_balance(new_balance, account_id)