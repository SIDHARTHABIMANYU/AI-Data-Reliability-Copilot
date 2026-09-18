import boto3
 
from backend.config.settings import settings
from backend.services.prompts.business_assistant import SYSTEM_PROMPT
from backend.schemas.chat_schema import ChatMessage

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=settings.AWS_REGION
)

def get_ai_response(messages:list[ChatMessage]) -> str:

    bedrock_messages = [
        {
            "role": message.role,
            "content": [
                {
                    "text": message.content
                }
            ]
        }
        for message in messages
    ]

    response = bedrock.converse(
       modelId=settings.BEDROCK_MODEL_ID,
       system=[
          {
              "text": SYSTEM_PROMPT
          }
    ],
        messages=bedrock_messages,
        inferenceConfig={
           "maxTokens": 500,
           "temperature": 0.7
    }
)

    return response["output"]["message"]["content"][0]["text"]