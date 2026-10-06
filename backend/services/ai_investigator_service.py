import json

from langchain_aws import ChatBedrockConverse

from backend.config.settings import settings
from backend.services.evidence_service import collect_incident_evidence


llm = ChatBedrockConverse(
    model=settings.BEDROCK_MODEL_ID,
    region_name=settings.AWS_REGION,
    max_tokens=1000,
    temperature=0.2,
)


def investigate_incident(incident_id: int) -> dict:
    evidence = collect_incident_evidence(incident_id)

    if "error" in evidence:
        return evidence

    prompt = f"""
You are an AI Data Reliability Investigator.

Investigate the data pipeline incident using ONLY the evidence
provided below.

Do not invent facts.
Do not assume missing information.

Return ONLY valid JSON.

The JSON must follow exactly this structure:

{{
    "summary": "brief explanation of what happened",
    "root_cause": "likely root cause based on evidence",
    "evidence": [
        "evidence point 1",
        "evidence point 2"
    ],
    "impact": [
        "affected downstream dataset or metric"
    ],
    "recommended_action": "practical next step for the data engineer",
    "confidence": "HIGH"
}}

The confidence value must be exactly one of:
HIGH
MEDIUM
LOW

Incident Evidence:

{evidence}
"""

    response = llm.invoke(prompt)

    content = response.content
    print("\n===== RAW AI RESPONSE =====")
    print(content)
    print("===========================\n")

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )
    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    try:
        investigation = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
        "AI returned an invalid JSON investigation response."
    )
    

    return investigation