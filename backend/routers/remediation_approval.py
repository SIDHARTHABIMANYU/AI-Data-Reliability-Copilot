from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.remediation_approval_service import (
    approve_remediation,
    reject_remediation,
)


router = APIRouter(
    prefix="/remediations",
    tags=["Remediation Approval"]
)


class ApprovalRequest(BaseModel):
    approved_by: str


@router.post("/{remediation_id}/approve")
def approve(
    remediation_id: int,
    request: ApprovalRequest
):
    result = approve_remediation(
        remediation_id=remediation_id,
        approved_by=request.approved_by
    )

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result


@router.post("/{remediation_id}/reject")
def reject(
    remediation_id: int,
    request: ApprovalRequest
):
    result = reject_remediation(
        remediation_id=remediation_id,
        rejected_by=request.approved_by
    )

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result