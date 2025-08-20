from app.repositories.agencia_repository import AgenciaRepository
from app.schemas.agencia_in import AgenciaIn
from app.views.agencia_out import AgenciaOut

class AgenciaService:
    def __init__(self, repository: AgenciaRepository):
        self.repository = repository

    async def get_all(self, limit, skip) -> list[AgenciaOut]:
        return await self.repository.get_all(limit, skip)

    async def get(self, id: int) -> AgenciaOut:
        return await self.repository.get_find_by_id(id)

    async def create(self, post: AgenciaIn) -> AgenciaOut:
        return await self.repository.create(post)