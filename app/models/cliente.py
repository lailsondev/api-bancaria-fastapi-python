import sqlalchemy as sa
from app.database import database, metadata


cliente = sa.Table(
    'clientes',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('sobrenome', sa.String(length=50), nullable=False),
    sa.Column('data_nascimento', sa.Date, nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False, index=True, unique=True),
)