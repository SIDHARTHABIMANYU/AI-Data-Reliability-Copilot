from fastapi import APIRouter, HTTPException
import logging

from backend.schemas.chat_schema import ChatRequest, ChatResponse
from backend.services.langchain_rag_service import generate_rag_answer


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        latest_message = request.messages[-1].content

        response = generate_rag_answer(latest_message)

        return {
            "message": response
        }

    except Exception:

        logger.exception("Error while processing chat request")

        raise HTTPException(
            status_code=500,
            detail="Unable to process your request."
        )