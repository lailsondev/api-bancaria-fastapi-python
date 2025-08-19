import sqlalchemy
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import database, metadata, DATABASE_URL

from app.controllers import agencia_controller, cliente_controller, transacao_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

    yield

    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(agencia_controller.router)
app.include_router(cliente_controller.router)
app.include_router(transacao_controller.router)