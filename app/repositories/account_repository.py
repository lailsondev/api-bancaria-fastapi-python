from databases import Database
from databases.interfaces import Record
import sqlalchemy as sa
from sqlalchemy import or_

from app.models.account import account
from app.schemas.account_in import AccountIn
from app.views.account_out import AccountOut


class AccountRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_account(self, post: AccountIn) -> AccountOut:
        query_account = account.insert().values(
            number=post.number,
            balance=post.balance,
            customer_id=post.customer_id,
            branch_id=post.branch_id,
        ).returning(
            account.c.id,
            account.c.number,
            account.c.balance,
            account.c.created_at,
            account.c.updated_at
        )

        new_account: Record = await self.db.fetch_one(query_account)

        return AccountOut(**dict(new_account))

    async def get_account(self, **kwargs) -> Record:
        conditions = []

        if 'number' in kwargs and kwargs['number'] is not None:
            conditions.append(account.c.number == kwargs['number'])

        if 'id' in kwargs and kwargs['id'] is not None:
            conditions.append(account.c.id == kwargs['id'])

        if 'target_id_account' in kwargs and kwargs['target_id_account'] is not None:
            conditions.append(account.c.id == kwargs['target_id_account'])

        query = sa.select(account).where(or_(*conditions))

        return await self.db.fetch_one(query)


    async def update_balance(self, new_balance, account_id):
        query = account.update().where(account.c.id == account_id).values(balance=new_balance)

        return await self.db.execute(query)