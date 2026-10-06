from pydantic import BaseModel
from typing import Literal


class RemediationResponse(BaseModel):
    incident_id: int
    remediation_id: int
    problem: str
    proposed_change: str
    validation_steps: list[str]
    risk: Literal["LOW", "MEDIUM", "HIGH"]
    requires_approval: bool