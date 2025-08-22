from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Case(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True, default=lambda: f"c_{uuid.uuid4().hex[:8]}")
    title = Column(String, nullable=False)
    narrative = Column(Text, nullable=False)
    status = Column(String, default="queued")
    result = Column(JSON, nullable=True)  # store final JSON result
    created_at = Column(String, nullable=False)

class Media(Base):
    __tablename__ = "media"
    id = Column(String, primary_key=True, default=lambda: f"m_{uuid.uuid4().hex[:8]}")
    case_id = Column(String, ForeignKey("cases.id"))
    uri = Column(Text)
    type = Column(String)
    meta = Column(JSON)
