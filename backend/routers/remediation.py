from fastapi import APIRouter, HTTPException

from backend.schemas.remediation_schema import RemediationResponse
from backend.services.remediation_service import suggest_remediation


router = APIRouter(
    prefix="/incidents",
    tags=["AI Remediation"]
)


@router.get(
    "/{incident_id}/remediation",
    response_model=RemediationResponse
)
def get_incident_remediation(incident_id: int):

    try:
        remediation = suggest_remediation(incident_id)

        if "error" in remediation:
            raise HTTPException(
                status_code=404,
                detail=remediation["error"]
            )

        return {
            "incident_id": incident_id,
            **remediation
        }

    except HTTPException:
        raise

    except Exception as error:
        print(f"Remediation error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate remediation."
        )