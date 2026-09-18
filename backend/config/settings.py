import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str
    BEDROCK_MODEL_ID: str
    AWS_BEARER_TOKEN_BEDROCK: str

    class Config:
        env_file = ".env"


settings = Settings()
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = settings.AWS_BEARER_TOKEN_BEDROCK