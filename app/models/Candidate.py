from uuid import uuid4 as _uuid

import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import UUID

from ..db import base as _database


class Candidate(_database.Base):
    __tablename__ = "candidate"
    id = _sql.Column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    name = _sql.Column(_sql.String, nullable=False, index=True)
    document_number = _sql.Column(_sql.String, unique=True, nullable=False, index=True)
    party = _sql.Column(_sql.String, nullable=True, index=True)
    votes = _sql.Column(_sql.Integer, nullable=False, default=0, server_default="0")
