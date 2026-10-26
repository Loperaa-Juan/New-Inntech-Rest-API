import uuid as _uuid

import pydantic as _pydantic


class VoterBase(_pydantic.BaseModel):
    name: str = _pydantic.Field(min_length=1)
    email: _pydantic.EmailStr

    model_config = _pydantic.ConfigDict(from_attributes=True)


class VoterCreate(VoterBase):
    pass


class Voter(VoterBase):
    id: _uuid.UUID
    has_voted: bool

    model_config = _pydantic.ConfigDict(from_attributes=True)
