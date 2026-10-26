import uuid as _uuid

import sqlalchemy.orm as _orm
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from ..models import Voter
from ..schemas import Voter as voter_schema


def create_voter(voter: voter_schema.VoterCreate, db: _orm.Session):
    voter_object = Voter(name=voter.name, email=voter.email)

    db.add(voter_object)
    try:
        db.commit()
        db.refresh(voter_object)
        return voter_object
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya está registrado")


def get_all_voters(db: _orm.Session):
    return db.query(Voter).all()


def get_voter_by_id(id: _uuid.UUID, db: _orm.Session):
    voter = db.query(Voter).filter(Voter.id == id).first()

    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    return voter


def delete_voter(id: _uuid.UUID, db: _orm.Session):
    voter = db.query(Voter).filter(Voter.id == id).first()

    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    db.delete(voter)
    db.commit()

    return {"message": "Votante eliminado exitosamente"}
