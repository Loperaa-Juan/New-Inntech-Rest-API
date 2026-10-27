import uuid as _uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...schemas import Voter as _voter
from ...schemas import errors as _errors
from ...schemas import pagination as _pagination
from ...services import auth_service as _authServices
from ...services import database as _databaseServices
from ...services import voter_service as _voterServices

# Todas las rutas de votantes requieren el token del administrador
router = APIRouter(
    dependencies=[Depends(_authServices.get_current_admin)],
    responses=_errors.UNAUTHORIZED,
)


@router.post(
    "",
    response_model=_voter.Voter,
    status_code=201,
    responses={
        409: _errors.error_response(
            "El email o el documento ya están registrados, o el documento pertenece a un candidato"
        )
    },
)
def create_voter(
    voter: _voter.VoterCreate, 
    db: Annotated[Session, Depends(_databaseServices.get_db)],
):
    voter = _voterServices.create_voter(voter, db=db)

    return voter


@router.get("", response_model=_pagination.Page[_voter.Voter])
def get_voters(
    filters: Annotated[_voter.VoterFilters, Query()],
    db: Annotated[Session, Depends(_databaseServices.get_db)],
):
    """
    Lista los votantes ordenados por nombre, paginados con `skip` y `limit` (máximo 100).
    `name` busca coincidencias parciales sin distinguir mayúsculas.
    """
    return _voterServices.get_all_voters(filters, db)


@router.get(
    "/{id}",
    response_model=_voter.Voter,
    responses={404: _errors.error_response("Votante no encontrado")},
)
def get_voter_by_id(
    id: _uuid.UUID, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    return _voterServices.get_voter_by_id(id, db)


@router.delete(
    "/{id}",
    status_code=204,
    responses={
        404: _errors.error_response("Votante no encontrado"),
        409: _errors.error_response("No se puede eliminar un votante que ya votó"),
    },
)
def delete_voter(
    id: _uuid.UUID, db: Annotated[Session, Depends(_databaseServices.get_db)]
):
    _voterServices.delete_voter(id, db)
