import uuid as _uuid

import pydantic as _pydantic


class CandidateBase(_pydantic.BaseModel):
    name: str = _pydantic.Field(min_length=1)
    document_number: str = _pydantic.Field(min_length=1)
    party: str | None = _pydantic.Field(default=None, min_length=1)

    model_config = _pydantic.ConfigDict(from_attributes=True)


class CandidateCreate(CandidateBase):
    pass


class Candidate(CandidateBase):
    id: _uuid.UUID
    votes: int

    model_config = _pydantic.ConfigDict(from_attributes=True)
