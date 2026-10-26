from uuid import uuid4 as _uuid

import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import UUID

from ..db import base as _database


class Vote(_database.Base):
    __tablename__ = "vote"
    id = _sql.Column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    voter_id = _sql.Column(
        UUID(as_uuid=True), _sql.ForeignKey("voter.id"), nullable=False, unique=True
    )
    candidate_id = _sql.Column(
        UUID(as_uuid=True), _sql.ForeignKey("candidate.id"), nullable=False
    )
