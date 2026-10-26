import uuid as _uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...schemas import Voter as _voter
from ...services import database as _databaseServices
from ...services import voter_service as _voterServices

router = APIRouter()


@router.post("", response_model=_voter.Voter, status_code=201)
def create_voter(
    voter: _voter.VoterCreate, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    voter = _voterServices.create_voter(voter, db=db)

    return voter


@router.get("", response_model=list[_voter.Voter])
def get_voters(db: Annotated[Session, Depends(_databaseServices.get_db)]):
    return _voterServices.get_all_voters(db)


@router.get("/{id}", response_model=_voter.Voter)
def get_voter_by_id(
    id: _uuid.UUID, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    return _voterServices.get_voter_by_id(id, db)


@router.delete("/{id}")
def delete_voter(
    id: _uuid.UUID, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    return _voterServices.delete_voter(id, db)
