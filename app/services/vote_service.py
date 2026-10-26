import uuid as _uuid

import sqlalchemy.orm as _orm
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models import Voter

from ..models import Candidate, Vote
from .candidate_service import get_candidate_by_id
from .voter_service import get_voter_by_id


def create_vote(voter_id: _uuid.UUID, candidate_id: _uuid.UUID, db: _orm.Session):
    # Validamos que el votante exista
    voter = get_voter_by_id(voter_id, db)

    # Validamos que el votante no haya votado aún
    if voter.has_voted is True:
        raise HTTPException(status_code=409, detail="El votante ya ha emitido su voto.")

    # Validamos que el candidato exista
    candidate = get_candidate_by_id(candidate_id, db)

    vote_object = Vote(voter_id=voter.id, candidate_id=candidate.id)

    # Marcamos al votante y sumamos el voto en la misma transacción.
    voter.has_voted = True
    candidate.votes = Candidate.votes + 1

    db.add(vote_object)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El votante ya ha emitido su voto.")

    db.refresh(vote_object)
    return vote_object


def get_all_votes(db: _orm.Session):
    return db.query(Vote).all()


def generate_statistics(db: _orm.Session):
    candidates = db.query(Candidate).order_by(Candidate.votes.desc()).all()
    total_votes = sum(candidate.votes for candidate in candidates)
    total_voters_voted = db.query(Voter).filter(Voter.has_voted.is_(True)).count()

    candidates_statistics = []
    for candidate in candidates:
        # Evitamos dividir entre cero cuando aún no hay votos
        percentage = (candidate.votes / total_votes * 100) if total_votes > 0 else 0.0
        candidates_statistics.append(
            {
                "candidate_id": candidate.id,
                "name": candidate.name,
                "votes": candidate.votes,
                "percentage": round(percentage, 2),
            }
        )

    return {
        "total_votes": total_votes,
        "total_voters_voted": total_voters_voted,
        "candidates": candidates_statistics,
    }
