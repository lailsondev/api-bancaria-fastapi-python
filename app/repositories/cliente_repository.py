import random

import sqlalchemy as sa
from databases import Database
from databases.interfaces import Record
from fastapi import HTTPException
from starlette import status

from app.models.agencia import agencia
from app.models.cliente import cliente
from app.models.conta import conta
from app.schemas.cliente_in import ClienteIn
from app.schemas.conta_in import ContaIn
from app.services.conta_service import ContaService
from app.views.cliente_com_conta_out import ClienteComContaOut


class ClienteRepository:
    def __init__(self, db: Database, conta_service: ContaService):
        self.db = db
        self.conta_service = conta_service


    async def get_clientes(self, limit, skip) -> list[ClienteComContaOut]:
        query = (
            sa.select(
                cliente.c.id.label('cliente_id'),
                cliente.c.nome.label('cliente_nome'),
                cliente.c.sobrenome.label('cliente_sobrenome'),
                cliente.c.data_nascimento.label('cliente_data_nascimento'),
                cliente.c.cpf.label('cliente_cpf'),
                conta.c.id.label('conta_id'),
                conta.c.numero.label('conta_numero'),
                conta.c.saldo.label('conta_saldo'),
                conta.c.created_at.label('conta_created_at'),
                conta.c.agencia_id.label('conta_agencia_id'),
            ).select_from(cliente).join(
                conta,
                conta.c.cliente_id == cliente.c.id
            ).limit(limit).offset(skip)
        )

        resultados: list[Record] = await self.db.fetch_all(query)

        clientes_com_conta = []
        for resultado in resultados:
            resultado_dict = dict(resultado)

            dados_cliente = {
                "id": resultado_dict["cliente_id"],
                "nome": resultado_dict["cliente_nome"],
                "sobrenome": resultado_dict["cliente_sobrenome"],
                "cpf": resultado_dict["cliente_cpf"],
                "data_nascimento": resultado_dict["cliente_data_nascimento"],
                "conta": {
                    "id": resultado_dict["conta_id"],
                    "numero": resultado_dict["conta_numero"],
                    "saldo": resultado_dict["conta_saldo"],
                    "created_at": resultado_dict["conta_created_at"],
                    "agencia_id": resultado_dict["conta_agencia_id"],
                }
            }

            clientes_com_conta.append(ClienteComContaOut.model_validate(dados_cliente))

        return clientes_com_conta

    async def criar_cliente(self, post: ClienteIn) -> ClienteComContaOut:

        async with self.db.transaction():

            if not await self.db.fetch_one(agencia.select().where(agencia.c.id == post.agencia_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A agência informada não existe.")


            query_cliente = cliente.insert().values(
                **post.model_dump(exclude={"agencia_id"})
            ).returning(
                cliente.c.id,
                cliente.c.nome,
                cliente.c.sobrenome,
                cliente.c.cpf,
                cliente.c.data_nascimento
            )

            novo_cliente: Record = await self.db.fetch_one(query_cliente)

            nova_conta = await self.conta_service.create_conta(
                ContaIn(
                    numero=random.randint(10 ** 14, 10 ** 15 - 1),
                    saldo=0.0,
                    cliente_id=novo_cliente["id"],
                    agencia_id=post.agencia_id
                )
            )

            return ClienteComContaOut(
                id=novo_cliente["id"],
                nome=novo_cliente["nome"],
                sobrenome=novo_cliente["sobrenome"],
                data_nascimento=novo_cliente["data_nascimento"],
                cpf=novo_cliente["cpf"],
                conta=nova_conta
            )