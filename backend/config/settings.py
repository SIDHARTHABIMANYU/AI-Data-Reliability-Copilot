import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str
    BEDROCK_MODEL_ID: str
    AWS_BEARER_TOKEN_BEDROCK: str
    PINECONE_API_KEY: str
    S3_BUCKET_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = settings.AWS_BEARER_TOKEN_BEDROCK