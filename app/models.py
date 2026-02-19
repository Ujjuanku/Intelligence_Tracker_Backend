from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    snapshots = relationship("Snapshot", back_populates="competitor", cascade="all, delete-orphan", order_by="desc(Snapshot.timestamp)")

class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    html_content = Column(Text, nullable=True) # Storing full HTML might be heavy, but requested
    text_content = Column(Text, nullable=True)
    diff_json = Column(JSON, nullable=True)
    ai_summary = Column(Text, nullable=True)

    competitor = relationship("Competitor", back_populates="snapshots")
