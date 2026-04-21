from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class IncidentCreate(BaseModel):
    title: str
    issue_description: str

class IncidentUpdate(BaseModel):
    status: str

class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    issue_description: str
    ai_response: Optional[str]
    severity: str
    status: str
    created_at: datetime
    owner_id: int

class DashboardResponse(BaseModel):
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    high_severity: int
    medium_severity: int
    low_severity: int