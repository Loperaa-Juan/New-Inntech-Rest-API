import os

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(_orm.DeclarativeBase):
    pass