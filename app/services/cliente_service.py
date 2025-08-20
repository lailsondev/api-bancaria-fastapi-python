from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_in import ClienteIn
from app.views.cliente_com_conta_out import ClienteComContaOut


class ClienteService:

    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    async def get_clientes(self, limit, skip) -> list[ClienteComContaOut]:
        return await self.repository.get_clientes(limit=limit, skip=skip)

    async def get_costumer(self, id) -> ClienteComContaOut:
        return await self.repository.get_cliente_by_id(id)

    async def criar_cliente(self, post: ClienteIn) -> ClienteComContaOut:
        return await self.repository.criar_cliente(post)