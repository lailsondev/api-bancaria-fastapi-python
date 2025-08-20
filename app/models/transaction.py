import sqlalchemy as sa
from sqlalchemy import func

from app.database import metadata


transaction = sa.Table(
    'transactions',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column('type', sa.String, nullable=False),
    sa.Column('value', sa.DECIMAL(10, 2), nullable=False),
    sa.Column('account_number', sa.BigInteger, nullable=False),
    sa.Column('date', sa.Date, server_default=sa.text("(CURRENT_DATE)")),
    sa.Column('hour', sa.Time, server_default=sa.text("(CURRENT_TIME)")),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
    sa.Column('source_account_id', sa.Integer, nullable=True),
    sa.Column('destination_account_id', sa.Integer, nullable=True),
    sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id', ondelete='CASCADE')),
)