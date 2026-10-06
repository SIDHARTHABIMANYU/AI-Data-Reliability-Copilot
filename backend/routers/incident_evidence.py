from fastapi import APIRouter, HTTPException

from backend.services.evidence_service import collect_incident_evidence


router = APIRouter(
    prefix="/incidents",
    tags=["Incident Evidence"]
)


@router.get("/{incident_id}/evidence")
def get_incident_evidence(incident_id: int):

    evidence = collect_incident_evidence(
        incident_id
    )

    if "error" in evidence:
        raise HTTPException(
            status_code=404,
            detail=evidence["error"]
        )

    return evidence