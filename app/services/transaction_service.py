from datetime import datetime, date
from decimal import Decimal

from fastapi import status, HTTPException

from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction_in import TransactionIn
from app.services.account_service import AccountService
from app.views.branch_out import BranchOut
from app.views.customer_out import CustomerOut
from app.views.account_out import AccountOut
from app.views.transaction_out import TransactionHistoryOut, TransactionOut


class TransactionService:
    def __init__(self, repository: TransactionRepository, account_service: AccountService):
        self.repository = repository
        self.account_service = account_service

    async def _check_source_account(self, account_number: int):
        source_account = await self.account_service.get_account(
            number=account_number
        )

        if not source_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")

        return source_account

    async def get_history(self, date, account_id, account_number, limit, skip) -> TransactionOut | list[TransactionOut]:

        if date:
            formated_date = datetime.strptime(date, "%d/%m/%Y").date()
            transactions = await self.repository.get_history(filter=formated_date, type_filter="date", limit=limit, skip=skip)
        elif account_id:
            transactions = await self.repository.get_history(filter=account_id, type_filter="account_id", limit=limit, skip=skip)
        elif account_number:
            transactions = await self.repository.get_history(filter=account_number, type_filter="account_number", limit=limit, skip=skip)
        else:
            transactions = await self.repository.get_history(filter=date.today(), type_filter="date", limit=limit, skip=skip)

        transaction_history_out = []

        for transaction in transactions:
            r_dict = dict(transaction)

            transaction_history_out.append(
                TransactionHistoryOut(
                    id=r_dict["transactions_id"],
                    type=r_dict["transactions_type"],
                    value=float(r_dict["transactions_value"]),
                    account_number=r_dict["transactions_account_number"],
                    date=r_dict["transactions_date"],
                    hour=r_dict["transactions_hour"],
                    created_at=r_dict["transactions_created_at"],
                    source_account_id=r_dict["transactions_source_account_id"],
                    destination_account_id=r_dict["transactions_destination_account_id"],
                    account=AccountOut(
                        id=r_dict["accounts_id"],
                        number=r_dict["accounts_number"],
                        balance=float(r_dict["accounts_balance"]),
                        created_at=r_dict["accounts_created_at"],
                    ),
                    customer=CustomerOut(
                        id=r_dict["customers_id"],
                        name=r_dict["customers_name"],
                        lastname=r_dict["customers_lastname"],
                        birth_date=r_dict["customers_birth_date"],
                        cpf=r_dict["customers_cpf"],
                    ),
                    branch=BranchOut(
                        id=r_dict["branchs_id"],
                        name=r_dict["branchs_name"],
                        number=r_dict["branchs_number"],
                        city=r_dict["branchs_city"],
                        state=r_dict["branchs_state"],
                    )
                )
            )

        return transaction_history_out

    async def create_transaction(self, post: TransactionIn):

        if post.type not in ('deposito', 'saque', 'transferencia'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="type de opreação inválida!")

        if post.value <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O valor do depósito deve ser positivo.")

        try:
            source_account = await self._check_source_account(post.account_number)

            if post.type == 'deposito':
                return await self._perform_deposit(post, source_account)
            elif post.type == 'saque':
                return await self._perform_withdrawal(post, source_account)
            else:
                return await self._perform_transfer(post, source_account)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    async def _perform_deposit(self, post: TransactionIn, source_account):
        new_balance = source_account["balance"] + Decimal(post.value)

        await self.account_service.update_balance(new_balance, source_account["id"])
        transaction_result = await self.repository.create_transaction(post, source_account)

        return await self._map_transaction_out(transaction_result, source_account, new_balance)

    async def _perform_withdrawal(self, post: TransactionIn, source_account):

        current_balance = Decimal(source_account["balance"])
        value_withdrawal = Decimal(str(post.value))

        if current_balance <= 0 or value_withdrawal > current_balance:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Não foi possível realizar o saque. Saldo onsuficiente: R$ {current_balance:.2f}.")

        new_balance = current_balance - value_withdrawal

        await self.account_service.update_balance(new_balance, source_account["id"])

        transaction_result = await self.repository.create_transaction(post, source_account)

        return await self._map_transaction_out(
            transaction_result, source_account, new_balance
        )

    async def _perform_transfer(self, post: TransactionIn, source_account):
        if post.destination_account_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Para efetuar uma transferência informe o ID da conta de destino.")

        value_source_account = Decimal(str(source_account["balance"]))

        if value_source_account <= 0 or post.value > value_source_account:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Você não tem saldo suficiente.")

        destination_account = await self.account_service.get_account(
            id=post.destination_account_id
        )

        if not destination_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta de destino não encontrada.")

        new_balance = value_source_account - Decimal(str(post.value))
        await self.account_service.update_balance(new_balance=new_balance, account_id=source_account["id"])


        new_balance_destination_account = destination_account["balance"] + Decimal(str(post.value))
        await self.account_service.update_balance(
            new_balance=new_balance_destination_account,
            account_id=destination_account["id"]
        )

        transaction_result = await self.repository.create_transaction(post, source_account)

        return await self._map_transaction_out(transaction_result, source_account, new_balance)

    async def _map_transaction_out(self, transaction_result, source_account, new_balance):
        transaction_result_dict = dict(transaction_result)

        return TransactionOut(
            id=transaction_result_dict["id"],
            type=transaction_result_dict["type"],
            value=transaction_result_dict["value"],
            account_number=transaction_result_dict["account_number"],
            date=transaction_result_dict["date"],
            hour=transaction_result_dict["hour"],
            source_account_id=source_account["id"],
            destination_account_id=source_account["id"],
            account=AccountOut(
                id=source_account["id"],
                number=source_account["number"],
                balance=new_balance,
                created_at=source_account["created_at"],
                updated_at=source_account["updated_at"],
            )
        )