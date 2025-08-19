import sqlalchemy as sa
from sqlalchemy import func

from app.database import metadata


transacao = sa.Table(
    'transacoes',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column('tipo', sa.String, nullable=False),
    sa.Column('valor', sa.DECIMAL(10, 2), nullable=False),
    sa.Column('numero_conta', sa.BigInteger, nullable=False),
    sa.Column('data', sa.Date, server_default=sa.text("(CURRENT_DATE)")),
    sa.Column('hora', sa.Time, server_default=sa.text("(CURRENT_TIME)")),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
    sa.Column('conta_id_origem', sa.Integer, nullable=True),
    sa.Column('conta_id_destino', sa.Integer, nullable=True),
    sa.Column('conta_id', sa.Integer, sa.ForeignKey('contas.id', ondelete='CASCADE')),
)