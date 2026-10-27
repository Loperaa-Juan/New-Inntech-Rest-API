import uuid as _uuid

import pydantic as _pydantic

from . import pagination as _pagination


class CandidateBase(_pydantic.BaseModel):
    name: str = _pydantic.Field(min_length=1)
    document_number: str = _pydantic.Field(min_length=1)
    party: str | None = _pydantic.Field(default=None, min_length=1)

    # Quita los espacios de los extremos: "   " no pasa min_length y " 111" es el mismo documento que "111"
    model_config = _pydantic.ConfigDict(from_attributes=True, str_strip_whitespace=True)


class CandidateCreate(CandidateBase):
    pass


class Candidate(CandidateBase):
    id: _uuid.UUID
    votes: int

    model_config = _pydantic.ConfigDict(from_attributes=True)


class CandidateFilters(_pagination.PaginationParams):
    # Búsquedas parciales y sin distinguir mayúsculas
    name: str | None = _pydantic.Field(default=None, min_length=1)
    party: str | None = _pydantic.Field(default=None, min_length=1)
