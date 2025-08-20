import sqlalchemy as sa
from sqlalchemy import func

from app.database import metadata


account = sa.Table(
    'accounts',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column('number', sa.BigInteger, nullable=False, index=True),
    sa.Column('balance', sa.DECIMAL(10, 2), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
    sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
    sa.Column('customer_id', sa.Integer, sa.ForeignKey('customers.id', ondelete='CASCADE')),
    sa.Column('branch_id', sa.Integer, sa.ForeignKey('branchs.id', ondelete='CASCADE'))
)