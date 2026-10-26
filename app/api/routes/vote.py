from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...schemas import Vote as _vote
from ...schemas import statistics as _statistics
from ...services import auth_service as _authServices
from ...services import database as _databaseServices
from ...services import vote_service as _voteServices

# Todas las rutas de votos requieren el token del administrador
router = APIRouter(dependencies=[Depends(_authServices.get_current_admin)])


@router.post("", response_model=_vote.Vote, status_code=201)
def create_vote(
    vote: _vote.VoteCreate,
    db: Annotated[Session, Depends(_databaseServices.get_db)],
):
    vote = _voteServices.create_vote(vote.voter_id, vote.candidate_id, db=db)

    return vote


@router.get("", response_model=list[_vote.Vote])
def get_votes(db: Annotated[Session, Depends(_databaseServices.get_db)]):
    return _voteServices.get_all_votes(db)


@router.get("/statistics", response_model=_statistics.VoteStatistics)
def get_statistics(db: Annotated[Session, Depends(_databaseServices.get_db)]):
    return _voteServices.generate_statistics(db)
