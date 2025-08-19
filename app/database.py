import os
from dotenv import load_dotenv
from databases import Database
import sqlalchemy as sa

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///api_bancaria.db")

database = Database(DATABASE_URL)

metadata = sa.MetaData()