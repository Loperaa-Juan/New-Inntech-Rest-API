import uuid as _uuid

import pydantic as _pydantic


class CandidateStatistics(_pydantic.BaseModel):
    candidate_id: _uuid.UUID
    name: str
    votes: int
    percentage: float


class VoteStatistics(_pydantic.BaseModel):
    total_votes: int
    total_voters_voted: int
    candidates: list[CandidateStatistics]
