from fastapi import APIRouter, HTTPException

from backend.schemas.investigation_schema import InvestigationResponse
from backend.services.ai_investigator_service import investigate_incident


router = APIRouter(
    prefix="/incidents",
    tags=["AI Investigation"]
)


@router.get(
    "/{incident_id}/investigation",
    response_model=InvestigationResponse
)
def get_incident_investigation(incident_id: int):

    try:
        investigation = investigate_incident(incident_id)

        if "error" in investigation:
            raise HTTPException(
                status_code=404,
                detail=investigation["error"]
            )

        return {
            "incident_id": incident_id,
            **investigation
        }

    except HTTPException:
        raise

    except Exception as error:
        print(f"Investigation error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to investigate incident."
        )