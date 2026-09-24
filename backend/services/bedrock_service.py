import boto3
 
from backend.config.settings import settings
from backend.services.prompts.business_assistant import SYSTEM_PROMPT
from backend.schemas.chat_schema import ChatMessage
from backend.services.rag_service import create_rag_prompt

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=settings.AWS_REGION
)

def get_ai_response(messages:list[ChatMessage]) -> str:

    latest_message = messages[-1].content

    rag_prompt = create_rag_prompt(latest_message)

    bedrock_messages = [
    {
        "role": "user",
        "content": [
            {
                "text": rag_prompt
            }
        ]
    }
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