from langchain_core.language_models.chat_models import BaseChatModel
from langchain_aws import ChatBedrockConverse
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.config.settings import settings


def get_llm() -> BaseChatModel:
    """
    Create the configured LLM for investigation
    and remediation services.
    """

    provider = settings.LLM_PROVIDER.strip().lower()

    if provider == "gemini":
        if not settings.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is required when LLM_PROVIDER=gemini."
            )

        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL_ID,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
            max_tokens=4096,
      )

    if provider == "bedrock":
        if not settings.BEDROCK_MODEL_ID:
            raise ValueError(
                "BEDROCK_MODEL_ID is required when LLM_PROVIDER=bedrock."
            )

        return ChatBedrockConverse(
            model=settings.BEDROCK_MODEL_ID,
            region_name=settings.AWS_REGION,
            api_key=settings.AWS_BEARER_TOKEN_BEDROCK,
            max_tokens=1000,
            temperature=0.2,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {provider}. "
        "Choose 'gemini' or 'bedrock'."
    )
