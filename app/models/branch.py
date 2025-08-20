import sqlalchemy as sa
from app.database import metadata


branch = sa.Table(
    "branchs",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, index=True),
    sa.Column("name", sa.String(50), nullable=False),
    sa.Column("number", sa.String(4), nullable=False, index=True),
    sa.Column("city", sa.String(50), nullable=False),
    sa.Column("state", sa.String(2), nullable=False),
)