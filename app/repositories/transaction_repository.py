import sqlalchemy as sa

from databases import Database
from databases.interfaces import Record

from app.models.branch import branch
from app.models.customer import customer
from app.models.account import account
from app.models.transaction import transaction
from app.schemas.transaction_in import TransactionIn
from app.views.transaction_out import TransactionOut, TransactionHistoryOut


class TransactionRepository:
    def __init__(self, db: Database):
        self.db = db


    async def get_history(self, filter, type_filter, limit, skip) -> TransactionOut | list[TransactionOut]:
        return await self._get_by_filter(filter=filter, type_filter=type_filter, limit=limit, skip=skip)

    async def _get_by_filter(self, filter, type_filter, limit, skip) -> Record | list[Record]:
        column_to_filter = transaction.c[type_filter]

        query = (
            sa.select(
                customer.c.id.label('customers_id'),
                customer.c.name.label('customers_name'),
                customer.c.lastname.label('customers_lastname'),
                customer.c.birth_date.label('customers_birth_date'),
                customer.c.cpf.label('customers_cpf'),
                account.c.id.label('accounts_id'),
                account.c.number.label('accounts_number'),
                account.c.balance.label('accounts_balance'),
                account.c.created_at.label('accounts_created_at'),
                branch.c.id.label('branchs_id'),
                branch.c.name.label('branchs_name'),
                branch.c.number.label('branchs_number'),
                branch.c.city.label('branchs_city'),
                branch.c.state.label('branchs_state'),
                transaction.c.id.label("transactions_id"),
                transaction.c.type.label("transactions_type"),
                transaction.c.value.label("transactions_value"),
                transaction.c.account_number.label("transactions_account_number"),
                transaction.c.date.label("transactions_date"),
                transaction.c.hour.label("transactions_hour"),
                transaction.c.created_at.label("transactions_created_at"),
                transaction.c.source_account_id.label("transactions_source_account_id"),
                transaction.c.destination_account_id.label("transactions_destination_account_id"),
            ).select_from(transaction).join(
                account,
                account.c.id == transaction.c.account_id
            ).join(
                customer,
                customer.c.id == account.c.customer_id
            ).join(
                branch,
                branch.c.id == account.c.branch_id
            ).where(column_to_filter == filter)
            .order_by(transaction.c.date, transaction.c.created_at.desc())
            .limit(limit)
            .offset(skip)
        )

        return await self.db.fetch_all(query)

    async def create_transaction(self, post: TransactionIn, source_account) -> Record:

        async with self.db.transaction():
            source_account_id = post.source_account_id if post.type == 'transferencia' else None
            destination_account_id = post.destination_account_id if post.type == 'transferencia' else None

            query_transaction = transaction.insert().values(
                type=post.type,
                value=post.value,
                account_number=post.account_number,
                source_account_id=source_account_id,
                destination_account_id=destination_account_id,
                account_id=source_account["id"],
            ).returning(
                transaction.c.id,
                transaction.c.type,
                transaction.c.value,
                transaction.c.account_number,
                transaction.c.date,
                transaction.c.hour,
                transaction.c.source_account_id,
                transaction.c.destination_account_id,
                transaction.c.account_id
            )

            return await self.db.fetch_one(query_transaction)