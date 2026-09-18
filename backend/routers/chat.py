from fastapi import APIRouter, HTTPException
import logging


from backend.schemas.chat_schema import ChatRequest, ChatResponse
from backend.services.bedrock_service import get_ai_response

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        response = get_ai_response(request.messages)

        return {
            "message": response
        }

    except Exception:
        logger.exception("Error while processing chat request")

    raise HTTPException(
        status_code=500,
        detail="Unable to process your request."
    )
