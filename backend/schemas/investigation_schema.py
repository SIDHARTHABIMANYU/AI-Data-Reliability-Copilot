from pydantic import BaseModel
from typing import Literal


class InvestigationResponse(BaseModel):
    incident_id: int
    summary: str
    root_cause: str
    evidence: list[str]
    impact: list[str]
    recommended_action: str
    confidence: Literal["HIGH", "MEDIUM", "LOW"]