import uuid as _uuid

import pydantic as _pydantic

from . import pagination as _pagination


class VoterBase(_pydantic.BaseModel):
    name: str = _pydantic.Field(min_length=1)
    email: _pydantic.EmailStr
    document_number: str = _pydantic.Field(min_length=1)

    model_config = _pydantic.ConfigDict(from_attributes=True)


class VoterCreate(VoterBase):
    pass


class Voter(VoterBase):
    id: _uuid.UUID
    has_voted: bool

    model_config = _pydantic.ConfigDict(from_attributes=True)


class VoterFilters(_pagination.PaginationParams):
    # Búsqueda parcial y sin distinguir mayúsculas
    name: str | None = _pydantic.Field(default=None, min_length=1)
    has_voted: bool | None = None
