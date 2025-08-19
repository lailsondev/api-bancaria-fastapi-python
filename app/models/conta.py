import sqlalchemy as sa
from sqlalchemy import func

from app.database import metadata


conta = sa.Table(
    'contas',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column('numero', sa.BigInteger, nullable=False, index=True),
    sa.Column('saldo', sa.DECIMAL(10, 2), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
    sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
    sa.Column('cliente_id', sa.Integer, sa.ForeignKey('clientes.id', ondelete='CASCADE')),
    sa.Column('agencia_id', sa.Integer, sa.ForeignKey('agencias.id', ondelete='CASCADE'))
)