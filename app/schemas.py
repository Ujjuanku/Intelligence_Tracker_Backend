from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List, Any

class CompetitorBase(BaseModel):
    url: HttpUrl

class CompetitorCreate(CompetitorBase):
    pass

class CompetitorResponse(CompetitorBase):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class SnapshotBase(BaseModel):
    timestamp: datetime
    ai_summary: Optional[str] = None
    diff_json: Optional[Any] = None

class SnapshotResponse(SnapshotBase):
    id: int
    competitor_id: int

    class Config:
        from_attributes = True

class CompetitorWithSnapshots(CompetitorResponse):
    pass
    # snapshots: List[SnapshotResponse] = [] # Optional to include logic
