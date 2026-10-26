import psycopg2
from ..db import base as _database

from ..models import Voter as _voterModel
from ..models import Vote as _voteModel
from ..models import Candidate as _candidateModel

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()