from uuid import uuid4 as _uuid

import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import UUID

from ..db import base as _database


class Voter(_database.Base):
    __tablename__ = "voter"
    id = _sql.Column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    name = _sql.Column(_sql.String, nullable=False, index=True)
    email = _sql.Column(_sql.String, unique=True, nullable=False, index=True)
    document_number = _sql.Column(_sql.String, unique=True, nullable=False, index=True)
    has_voted = _sql.Column(_sql.Boolean, nullable=False, default=False)
