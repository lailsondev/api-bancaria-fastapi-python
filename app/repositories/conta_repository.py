from databases import Database
from databases.interfaces import Record
import sqlalchemy as sa
from sqlalchemy import or_

from app.models.conta import conta
from app.schemas.conta_in import ContaIn, ContaUnicaIn
from app.views.conta_out import ContaOut


class ContaRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_conta(self, conta: ContaIn) -> ContaOut:
        query_conta = conta.insert().values(
            numero=conta.numero,
            saldo=conta.saldo,
            cliente_id=conta.cliente_id,
            agencia_id=conta.agencia_id,
        ).returning(
            conta.c.id,
            conta.c.numero,
            conta.c.saldo,
            conta.c.created_at,
            conta.c.updated_at
        )

        nova_conta: Record = await self.db.fetch_one(query_conta)

        return ContaOut(**dict(nova_conta))

    async def get_conta(self, **kwargs) -> Record:
        condicoes = []

        if 'numero' in kwargs and kwargs['numero'] is not None:
            condicoes.append(conta.c.numero == kwargs['numero'])

        if 'conta_id_destino' in kwargs and kwargs['conta_id_destino'] is not None:
            condicoes.append(conta.c.id == kwargs['conta_id_destino'])

        query = sa.select(conta).where(or_(*condicoes))

        return await self.db.fetch_one(query)


    async def update_saldo(self, novo_saldo, conta_id):
        query = conta.update().where(conta.c.id == conta_id).values(saldo=novo_saldo)

        return await self.db.execute(query)