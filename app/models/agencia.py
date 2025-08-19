import sqlalchemy as sa
from app.database import metadata


agencia = sa.Table(
    "agencias",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column("nome", sa.String(50), nullable=False),
    sa.Column("numero", sa.String(4), nullable=False, index=True),
    sa.Column("cidade", sa.String(50), nullable=False),
    sa.Column("estado", sa.String(2), nullable=False),
)