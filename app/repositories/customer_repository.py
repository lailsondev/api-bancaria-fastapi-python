import random

import sqlalchemy as sa
from databases import Database
from databases.interfaces import Record
from fastapi import HTTPException
from starlette import status

from app.models.branch import branch
from app.models.customer import customer
from app.models.account import account
from app.schemas.customer_in import CustomerIn
from app.schemas.account_in import AccountIn
from app.services.account_service import AccountService
from app.views.customer_with_account_out import CustomerWithAccountOut
from app.views.account_out import AccountOut


class CustomerRepository:
    def __init__(self, db: Database, account_service: AccountService):
        self.db = db
        self.account_service = account_service


    async def get_customers(self, limit, skip) -> list[CustomerWithAccountOut]:
        query = self._return_query_costumer_with_account().limit(limit).offset(skip)

        results: list[Record] = await self.db.fetch_all(query)

        customers_with_accounts: list[CustomerWithAccountOut] = []
        for result in results:
            result_dict = dict(result)

            customers_data = {
                "id": result_dict["account_id"],
                "name": result_dict["account_name"],
                "lastname": result_dict["account_lastname"],
                "cpf": result_dict["account_cpf"],
                "birth_date": result_dict["account_birth_date"],
                "account": {
                    "id": result_dict["account_id"],
                    "number": result_dict["account_number"],
                    "balance": result_dict["account_balance"],
                    "created_at": result_dict["account_created_at"],
                    "branch_id": result_dict["account_branch_id"],
                }
            }

            customers_with_accounts.append(CustomerWithAccountOut.model_validate(customers_data))

        return customers_with_accounts

    async def find_by_id(self, id: int) -> CustomerWithAccountOut:
        query = self._return_query_costumer_with_account().where(customer.c.id == id)

        row: Record = await self.db.fetch_one(query)
        row_dict = dict(row)

        account_out = AccountOut(
            id=row_dict["account_id"],
            number=row_dict["account_number"],
            balance=row_dict["account_balance"],
            created_at=row_dict["account_created_at"],
        )

        return CustomerWithAccountOut(
            id=row_dict["account_id"],
            name=row_dict["account_name"],
            lastname=row_dict["account_lastname"],
            birth_date=row_dict["account_birth_date"],
            cpf=row_dict["account_cpf"],
            account=account_out
        )

    async def create_customer(self, post: CustomerIn) -> CustomerWithAccountOut:

        async with self.db.transaction():

            if not await self.db.fetch_one(branch.select().where(branch.c.id == post.branch_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A agência informada não existe.")


            query_customer = customer.insert().values(
                **post.model_dump(exclude={"branch_id"})
            ).returning(
                customer.c.id,
                customer.c.name,
                customer.c.lastname,
                customer.c.birth_date,
                customer.c.cpf
            )

            new_customer: Record = await self.db.fetch_one(query_customer)

            new_account = await self.account_service.create_account(
                AccountIn(
                    number=random.randint(10 ** 14, 10 ** 15 - 1),
                    balance=0.0,
                    customer_id=new_customer["id"],
                    branch_id=post.branch_id
                )
            )

            return CustomerWithAccountOut(
                id=new_customer["id"],
                name=new_customer["name"],
                lastname=new_customer["lastname"],
                birth_date=new_customer["birth_date"],
                cpf=new_customer["cpf"],
                account=new_account
            )

    def _return_query_costumer_with_account(self):
        return sa.select(
                customer.c.id.label('account_id'),
                customer.c.name.label('account_name'),
                customer.c.lastname.label('account_lastname'),
                customer.c.birth_date.label('account_birth_date'),
                customer.c.cpf.label('account_cpf'),
                account.c.id.label('account_id'),
                account.c.number.label('account_number'),
                account.c.balance.label('account_balance'),
                account.c.created_at.label('account_created_at'),
                account.c.branch_id.label('account_branch_id'),
        ).select_from(customer).join(
            account,
            account.c.customer_id == customer.c.id
        )