from typing import Optional

from databases.interfaces import Record

from app.repositories.conta_repository import ContaRepository
from app.schemas.conta_in import ContaIn, ContaUnicaIn
from app.views.conta_out import ContaOut


class ContaService:
    def __init__(self, repository: ContaRepository):
        self.repository = repository

    async def create_conta(self, post: ContaIn) -> ContaOut:
        return await self.repository.create_conta(post)

    async def obter_conta(self, **kwargs) -> Optional[Record]:
        return await self.repository.get_conta(**kwargs)

    async def update_saldo(self, novo_saldo, conta_id):
        return await self.repository.update_saldo(novo_saldo, conta_id)