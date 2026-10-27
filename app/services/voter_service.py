import uuid as _uuid

import sqlalchemy.orm as _orm
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from ..models import Candidate, Voter
from ..schemas import Voter as voter_schema


def create_voter(voter: voter_schema.VoterCreate, db: _orm.Session):
    # Un candidato no puede ser votante
    if (
        db.query(Candidate)
        .filter(Candidate.document_number == voter.document_number)
        .first()
    ):
        raise HTTPException(
            status_code=409,
            detail="El documento pertenece a un candidato. Un candidato no puede ser votante",
        )

    if db.query(Voter).filter(Voter.email == voter.email).first():
        raise HTTPException(status_code=409, detail="El email ya está registrado")

    if db.query(Voter).filter(Voter.document_number == voter.document_number).first():
        raise HTTPException(
            status_code=409, detail="El número de documento ya está registrado"
        )

    voter_object = Voter(
        name=voter.name,
        email=voter.email,
        document_number=voter.document_number,
    )

    db.add(voter_object)
    try:
        db.commit()
        db.refresh(voter_object)
        return voter_object
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El votante ya está registrado")


def get_all_voters(filters: voter_schema.VoterFilters, db: _orm.Session):
    query = db.query(Voter)

    if filters.name is not None:
        # autoescape hace que "%" y "_" se busquen como texto y no como comodines
        query = query.filter(Voter.name.icontains(filters.name, autoescape=True))

    if filters.has_voted is not None:
        query = query.filter(Voter.has_voted == filters.has_voted)

    # Contamos antes de paginar para que el total refleje los filtros, no solo la página
    total = query.count()

    # Sin un orden fijo, PostgreSQL puede repetir o saltarse filas entre páginas.
    # El id desempata a los votantes con el mismo nombre.
    items = (
        query.order_by(Voter.name, Voter.id)
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


def get_voter_by_id(id: _uuid.UUID, db: _orm.Session):
    voter = db.query(Voter).filter(Voter.id == id).first()

    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    return voter


def delete_voter(id: _uuid.UUID, db: _orm.Session):
    voter = get_voter_by_id(id, db)

    db.delete(voter)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar un votante que ya votó",
        )
