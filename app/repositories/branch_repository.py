from databases import Database
from databases.interfaces import Record

from app.models.branch import branch
from app.schemas.branch_in import BranchIn
from app.views.branch_out import BranchOut


class BranchRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_all(self, limit, skip) -> list[BranchOut]:
        query = branch.select().limit(limit).offset(skip)

        rows: list[Record] = await self.db.fetch_all(query)

        return [BranchOut(**dict(row)) for row in rows]

    async def find_by_id(self, id: int) -> BranchOut:
        query = branch.select().where(branch.c.id == id)

        row: Record = await self.db.fetch_one(query)

        return BranchOut(**dict(row))


    async def create(self, post: BranchIn) -> BranchOut:
        query = branch.insert().values(**post.model_dump())

        id: list[Record] = await self.db.execute(query)

        row = await self.db.fetch_one(branch.select().where(branch.c.id == id))
        return BranchOut(**dict(row))