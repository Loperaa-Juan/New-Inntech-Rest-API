import uuid as _uuid

import sqlalchemy.orm as _orm
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from ..models import Candidate, Voter
from ..schemas import Candidate as candidate_schema


def create_candidate(candidate: candidate_schema.CandidateCreate, db: _orm.Session):
    # Un votante no puede ser candidato
    if (
        db.query(Voter)
        .filter(Voter.document_number == candidate.document_number)
        .first()
    ):
        raise HTTPException(
            status_code=409,
            detail="El documento pertenece a un votante. Un votante no puede ser candidato",
        )

    if (
        db.query(Candidate)
        .filter(Candidate.document_number == candidate.document_number)
        .first()
    ):
        raise HTTPException(
            status_code=409, detail="El número de documento ya está registrado"
        )

    candidate_object = Candidate(
        name=candidate.name,
        document_number=candidate.document_number,
        party=candidate.party,
    )

    db.add(candidate_object)
    try:
        db.commit()
        db.refresh(candidate_object)
        return candidate_object
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El candidato ya está registrado")


def get_all_candidates(db: _orm.Session):
    return db.query(Candidate).all()


def get_candidate_by_id(id: _uuid.UUID, db: _orm.Session):
    candidate = db.query(Candidate).filter(Candidate.id == id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    return candidate


def delete_candidate(id: _uuid.UUID, db: _orm.Session):
    candidate = get_candidate_by_id(id, db)

    db.delete(candidate)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar un candidato que ya tiene votos",
        )

    return {"message": "Candidato eliminado exitosamente"}
