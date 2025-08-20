from databases import Database
from databases.interfaces import Record

from app.models.agencia import agencia
from app.schemas.agencia_in import AgenciaIn
from app.views.agencia_out import AgenciaOut


class AgenciaRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_all(self, limit, skip) -> list[AgenciaOut]:
        query = agencia.select().limit(limit).offset(skip)

        rows: list[Record] = await self.db.fetch_all(query)

        return [AgenciaOut(**dict(row)) for row in rows]

    async def get_find_by_id(self, id: int) -> AgenciaOut:
        query = agencia.select().where(agencia.c.id == id)

        row: Record = await self.db.fetch_one(query)

        return AgenciaOut(**dict(row))


    async def create(self, post: AgenciaIn) -> AgenciaOut:
        query = agencia.insert().values(**post.model_dump())

        id: list[Record] = await self.db.execute(query)

        row = await self.db.fetch_one(agencia.select().where(agencia.c.id == id))
        return AgenciaOut(**dict(row))