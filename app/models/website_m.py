from sqlalchemy import Column, String, Text, ARRAY, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql.sqltypes import Float
from pgvector.sqlalchemy import Vector
import uuid

from ..core.db import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(UUID(
                as_uuid=True), 
                primary_key=True, 
                default=uuid.uuid4, 
                index=True
                )
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    tags = Column(ARRAY(Text), default=[])
    screenshot_url = Column(Text, nullable=True)
    embedding = Column(Vector(384), nullable=True)  
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
