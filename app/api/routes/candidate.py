import uuid as _uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...schemas import Candidate as _candidate
from ...services import candidate_service as _candidateServices
from ...services import database as _databaseServices

router = APIRouter()


@router.post("", response_model=_candidate.Candidate, status_code=201)
def create_candidate(
    candidate: _candidate.CandidateCreate,
    db: Annotated[Session, Depends(_databaseServices.get_db)],
):
    candidate = _candidateServices.create_candidate(candidate, db=db)

    return candidate


@router.get("", response_model=list[_candidate.Candidate])
def get_candidates(db: Annotated[Session, Depends(_databaseServices.get_db)]):
    return _candidateServices.get_all_candidates(db)


@router.get("/{id}", response_model=_candidate.Candidate)
def get_candidate_by_id(
    id: _uuid.UUID, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    return _candidateServices.get_candidate_by_id(id, db)


@router.delete("/{id}")
def delete_candidate(
    id: _uuid.UUID, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    return _candidateServices.delete_candidate(id, db)
