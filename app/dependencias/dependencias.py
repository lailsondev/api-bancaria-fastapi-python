from databases import Database
from fastapi import Depends

from app.database import database
from app.repositories.agencia_repository import AgenciaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.conta_repository import ContaRepository
from app.repositories.transacao_repository import TransacaoRepository
from app.services.agencia_service import AgenciaService
from app.services.cliente_service import ClienteService
from app.services.conta_service import ContaService
from app.services.transacao_service import TransacaoService


def get_database_connection():
    return database


async def get_conta_repository(db: Database = Depends(get_database_connection)):
    return ContaRepository(db)


async def fabrica_conta_service(conta_repository: ContaRepository = Depends(get_conta_repository)):
    return ContaService(conta_repository)

async def get_agencia_repository(db: Database = Depends(get_database_connection)):
    return AgenciaRepository(db)

async def fabrica_agencia_service(agencia_repository: AgenciaRepository = Depends(get_agencia_repository)):
    return AgenciaService(agencia_repository)

async def get_transacao_repository(db: Database = Depends(get_database_connection)):
    return TransacaoRepository(db)

async def fabrica_transacao_service(
        transacao_repository: TransacaoRepository = Depends(get_transacao_repository),
        conta_service: ContaService = Depends(fabrica_conta_service)
):
    return TransacaoService(transacao_repository, conta_service)


async def get_cliente_repository(
    db: Database = Depends(get_database_connection),
    conta_service: ContaService = Depends(fabrica_conta_service)
):
    return ClienteRepository(db, conta_service)


async def fabrica_cliente_service(cliente_repository: ClienteRepository = Depends(get_cliente_repository)):
    return ClienteService(cliente_repository)
