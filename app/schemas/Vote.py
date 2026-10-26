import uuid as _uuid

import pydantic as _pydantic


class VoteBase(_pydantic.BaseModel):
    voter_id: _uuid.UUID = _pydantic.Field(alias="voter_id")
    candidate_id: _uuid.UUID = _pydantic.Field(alias="candidate_id")

    model_config = _pydantic.ConfigDict(from_attributes=True)


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: _uuid.UUID

    model_config = _pydantic.ConfigDict(from_attributes=True)
