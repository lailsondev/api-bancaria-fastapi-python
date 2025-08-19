from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel

from app.views.agencia_out import AgenciaOut
from app.views.cliente_out import ClienteOut
from app.views.conta_out import ContaOut


class TransacaoOut(BaseModel):
    id: int
    tipo: str
    valor: float
    numero_conta: int
    data: date
    hora: time
    created_at: Optional[datetime] = None
    conta_id_origem: Optional[int] = None
    conta_id_destino: Optional[int] = None
    conta_id: Optional[int] = None

    conta: ContaOut


class TransacaoHistoricoOut(BaseModel):
    id: int
    tipo: str
    valor: float
    numero_conta: int
    data: date
    hora: time
    created_at: Optional[datetime] = None
    conta_id_origem: Optional[int] = None
    conta_id_destino: Optional[int] = None
    conta_id: Optional[int] = None

    conta: ContaOut
    cliente: ClienteOut
    agencia: AgenciaOut

    # cliente.c.id.label('clientes_id'),
    # cliente.c.nome.label('clientes_nome'),
    # cliente.c.sobrenome.label('clientes_sobrenome'),
    # cliente.c.data_nascimento.label('clientes_data_nascimento'),
    # cliente.c.cpf.label('clientes_cpf'),
    # conta.c.id.label('contas_id'),
    # conta.c.numero.label('contas_numero'),
    # conta.c.saldo.label('contas_saldo'),
    # agencia.c.id.label('agencias_id'),
    # agencia.c.nome.label('agencias_nome'),
    # agencia.c.numero.label('agencias_numero'),
    # agencia.c.cidade.label('agencias_cidade'),
    # agencia.c.estado.label('agencias_estado'),
    # transacao.c.id.label("transacoes_id"),
    # transacao.c.tipo.label("transacoes_tipo"),
    # transacao.c.valor.label("transacoes_valor"),
    # transacao.c.numero_conta.label("transacoes_numero_conta"),
    # transacao.c.data.label("transacoes_data"),
    # transacao.c.hora.label("transacoes_hora"),
    # transacao.c.created_at.label("transacoes_created_at"),
    # transacao.c.conta_id_origem.label("transacoes_conta_id_origem"),
    # transacao.c.conta_id_destino.label("transacoes_conta_id_destino"),