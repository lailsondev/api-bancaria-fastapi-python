from decimal import Decimal

import sqlalchemy as sa

from databases import Database
from databases.interfaces import Record
from fastapi import HTTPException, status

from app.models.agencia import agencia
from app.models.cliente import cliente
from app.models.conta import conta
from app.models.transacao import transacao
from app.schemas.transacao_in import TransacaoIn
from app.views.agencia_out import AgenciaOut
from app.views.cliente_out import ClienteOut
from app.views.conta_out import ContaOut
from app.views.transacao_out import TransacaoOut, TransacaoHistoricoOut


class TransacaoRepository:
    def __init__(self, db: Database):
        self.db = db


    async def get_historico(self, filtro, tipo_filtro, limit, skip) -> TransacaoOut | list[TransacaoOut]:
        return await self._get_by_filter(filtro=filtro, tipo_filtro=tipo_filtro, limit=limit, skip=skip)


    async def _get_by_filter(self, filtro, tipo_filtro, limit, skip) -> Record | list[Record]:
        coluna_a_filtrar = transacao.c[tipo_filtro]

        query = (
            sa.select(
                cliente.c.id.label('clientes_id'),
                cliente.c.nome.label('clientes_nome'),
                cliente.c.sobrenome.label('clientes_sobrenome'),
                cliente.c.data_nascimento.label('clientes_data_nascimento'),
                cliente.c.cpf.label('clientes_cpf'),
                conta.c.id.label('contas_id'),
                conta.c.numero.label('contas_numero'),
                conta.c.saldo.label('contas_saldo'),
                conta.c.created_at.label('contas_created_at'),
                agencia.c.id.label('agencias_id'),
                agencia.c.nome.label('agencias_nome'),
                agencia.c.numero.label('agencias_numero'),
                agencia.c.cidade.label('agencias_cidade'),
                agencia.c.estado.label('agencias_estado'),
                transacao.c.id.label("transacoes_id"),
                transacao.c.tipo.label("transacoes_tipo"),
                transacao.c.valor.label("transacoes_valor"),
                transacao.c.numero_conta.label("transacoes_numero_conta"),
                transacao.c.data.label("transacoes_data"),
                transacao.c.hora.label("transacoes_hora"),
                transacao.c.created_at.label("transacoes_created_at"),
                transacao.c.conta_id_origem.label("transacoes_conta_id_origem"),
                transacao.c.conta_id_destino.label("transacoes_conta_id_destino"),
            ).select_from(transacao).join(
                conta,
                conta.c.id == transacao.c.conta_id
            ).join(
                cliente,
                cliente.c.id == conta.c.cliente_id
            ).join(
                agencia,
                agencia.c.id == conta.c.agencia_id
            ).where(coluna_a_filtrar == filtro)
            .order_by(transacao.c.data, transacao.c.created_at.desc())
            .limit(limit)
            .offset(skip)
        )

        return await self.db.fetch_all(query)

    async def create_transacao(self, post: TransacaoIn, conta_origem) -> Record:

        async with self.db.transaction():
            conta_id_origem = post.conta_id_origem or None
            conta_id_destino = post.conta_id_destino or None

            query_transacao = transacao.insert().values(
                tipo=post.tipo,
                valor=post.valor,
                numero_conta=post.numero_conta,
                conta_id_origem=conta_id_origem,
                conta_id_destino=conta_id_destino,
                conta_id=conta_origem["id"],
            ).returning(
                transacao.c.id,
                transacao.c.tipo,
                transacao.c.valor,
                transacao.c.numero_conta,
                transacao.c.data,
                transacao.c.hora,
                transacao.c.conta_id_origem,
                transacao.c.conta_id_destino,
                transacao.c.conta_id
            )

            return await self.db.fetch_one(query_transacao)