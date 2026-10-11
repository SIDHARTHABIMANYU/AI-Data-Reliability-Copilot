from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, StringConstraints

from backend.services.remediation_approval_service import (
    approve_remediation,
    reject_remediation,
)


router = APIRouter(
    prefix="/remediations",
    tags=["Remediation Approval"],
)


ApproverName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approved_by: ApproverName


def _raise_remediation_error(message: str) -> None:
    """Convert remediation service errors into appropriate HTTP errors."""
    if message == "Remediation not found":
        raise HTTPException(
            status_code=404,
            detail=message,
        )

    raise HTTPException(
        status_code=409,
        detail=message,
    )


@router.post("/{remediation_id}/approve")
def approve(
    remediation_id: int,
    request: ApprovalRequest,
) -> dict:
    """Approve a pending remediation recommendation."""
    if remediation_id < 1:
        raise HTTPException(
            status_code=422,
            detail="remediation_id must be positive",
        )

    result = approve_remediation(
        remediation_id=remediation_id,
        approved_by=request.approved_by,
    )

    if "error" in result:
        _raise_remediation_error(result["error"])

    return result


@router.post("/{remediation_id}/reject")
def reject(
    remediation_id: int,
    request: ApprovalRequest,
) -> dict:
    """Reject a pending remediation recommendation."""
    if remediation_id < 1:
        raise HTTPException(
            status_code=422,
            detail="remediation_id must be positive",
        )

    result = reject_remediation(
        remediation_id=remediation_id,
        rejected_by=request.approved_by,
    )

    if "error" in result:
        _raise_remediation_error(result["error"])

    return result