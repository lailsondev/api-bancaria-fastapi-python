from app.repositories.branch_repository import BranchRepository
from app.schemas.branch_in import BranchIn
from app.views.branch_out import BranchOut

class BranchService:
    def __init__(self, repository: BranchRepository):
        self.repository = repository

    async def get_all(self, limit, skip) -> list[BranchOut]:
        return await self.repository.get_all(limit, skip)

    async def get(self, id: int) -> BranchOut:
        return await self.repository.find_by_id(id)

    async def create(self, post: BranchIn) -> BranchOut:
        return await self.repository.create(post)