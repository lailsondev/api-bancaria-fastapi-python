import sqlalchemy as sa
from app.database import database, metadata


customer = sa.Table(
    'customers',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('lastname', sa.String(length=50), nullable=False),
    sa.Column('birth_date', sa.Date, nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False, index=True, unique=True),
)