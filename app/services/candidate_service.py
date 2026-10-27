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


def get_all_candidates(filters: candidate_schema.CandidateFilters, db: _orm.Session):
    query = db.query(Candidate)

    if filters.name is not None:
        # autoescape hace que "%" y "_" se busquen como texto y no como comodines
        query = query.filter(Candidate.name.icontains(filters.name, autoescape=True))

    if filters.party is not None:
        query = query.filter(Candidate.party.icontains(filters.party, autoescape=True))

    # Contamos antes de paginar para que el total refleje los filtros, no solo la página
    total = query.count()

    # Sin un orden fijo, PostgreSQL puede repetir o saltarse filas entre páginas.
    # El id desempata a los candidatos con el mismo nombre.
    items = (
        query.order_by(Candidate.name, Candidate.id)
        .offset(filters.skip)
        .limit(filters.limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "skip": filters.skip,
        "limit": filters.limit,
    }


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
