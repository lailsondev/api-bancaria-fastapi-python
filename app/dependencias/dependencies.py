from databases import Database
from fastapi import Depends

from app.database import database
from app.repositories.branch_repository import BranchRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.branch_service import BranchService
from app.services.customer_service import CustomerService
from app.services.account_service import AccountService
from app.services.transaction_service import TransactionService


def get_database_connection():
    return database


async def get_account_repository(db: Database = Depends(get_database_connection)):
    return AccountRepository(db)


async def factory_account_service(account_repository: AccountRepository = Depends(get_account_repository)):
    return AccountService(account_repository)

async def get_branch_repository(db: Database = Depends(get_database_connection)):
    return BranchRepository(db)

async def factory_branch_service(branch_repository: BranchRepository = Depends(get_branch_repository)):
    return BranchService(branch_repository)

async def get_transaction_repository(db: Database = Depends(get_database_connection)):
    return TransactionRepository(db)

async def factory_transaction_service(
        transaction_repository: TransactionRepository = Depends(get_transaction_repository),
        account_service: AccountService = Depends(factory_account_service)
):
    return TransactionService(transaction_repository, account_service)


async def get_cusutomer_repository(
    db: Database = Depends(get_database_connection),
    account_service: AccountService = Depends(factory_account_service)
):
    return CustomerRepository(db, account_service)


async def factory_customer_service(cusutomer_repository: CustomerRepository = Depends(get_cusutomer_repository)):
    return CustomerService(cusutomer_repository)
