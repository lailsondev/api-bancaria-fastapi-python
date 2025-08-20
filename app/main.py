import sqlalchemy
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import database, metadata, DATABASE_URL

from app.controllers import auth_controller, branch_controller, customer_controller, transaction_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

    yield

    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_controller.router)
app.include_router(branch_controller.router)
app.include_router(customer_controller.router)
app.include_router(transaction_controller.router)