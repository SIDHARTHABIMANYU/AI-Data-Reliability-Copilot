from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # AWS Bedrock — optional when using Gemini
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = ""
    AWS_BEARER_TOKEN_BEDROCK: str | None = None

    # Gemini — optional when using Bedrock
    GOOGLE_API_KEY: str | None = None
    GEMINI_MODEL_ID: str = "gemini-2.5-flash"

    # Existing services
    PINECONE_API_KEY: str
    S3_BUCKET_NAME: str

    # Select the active LLM provider
    LLM_PROVIDER: str = "gemini"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
