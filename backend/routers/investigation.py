from fastapi import APIRouter, HTTPException

from backend.schemas.investigation_schema import InvestigationResponse
from backend.services.reliability.graph import run_reliability_graph


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
        result = run_reliability_graph(
            incident_id
        )

        evidence = result.get(
            "evidence",
            {}
        )

        if "error" in evidence:
            raise HTTPException(
                status_code=404,
                detail=evidence["error"]
            )

        analysis = result.get(
            "analysis",
            {}
        )

        return {
            "incident_id": incident_id,
            **analysis
        }

    except HTTPException:
        raise

    except Exception:
       import traceback

       traceback.print_exc()

       raise HTTPException(
          status_code=500,
          detail="Unable to investigate incident."
    )