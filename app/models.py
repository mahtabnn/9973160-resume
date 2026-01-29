from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .db import Base

class ProjectRequest(Base):
    __tablename__ = "project_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="new")
    admin_notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)