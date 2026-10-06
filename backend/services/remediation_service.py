import json

from langchain_aws import ChatBedrockConverse

from backend.config.settings import settings
from backend.services.evidence_service import collect_incident_evidence
from backend.services.remediation_approval_service import (
    create_pending_remediation
)

llm = ChatBedrockConverse(
    model=settings.BEDROCK_MODEL_ID,
    region_name=settings.AWS_REGION,
    max_tokens=1000,
    temperature=0.2,
)


def suggest_remediation(incident_id: int) -> dict:
    evidence = collect_incident_evidence(incident_id)

    if "error" in evidence:
        return evidence

    prompt = f"""
You are an AI Data Reliability Remediation Assistant.

Your job is to suggest a safe remediation for a data pipeline
incident using ONLY the evidence provided below.

Do not invent facts.
Do not automatically assume that two columns are equivalent.
Do not recommend a production change unless the evidence supports it.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "problem": "What is wrong",
    "proposed_change": "What change should be considered",
    "validation_steps": [
        "Validation step 1",
        "Validation step 2",
        "Validation step 3"
    ],
    "risk": "LOW",
    "requires_approval": true
}}

The risk must be exactly one of:

LOW
MEDIUM
HIGH

For production data changes, requires_approval should normally
be true.

Incident Evidence:

{evidence}
"""

    response = llm.invoke(prompt)

    content = response.content

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
        remediation = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
            "AI returned an invalid JSON remediation response."
        )
    remediation_id = create_pending_remediation(
        incident_id=incident_id,
        proposed_change=remediation["proposed_change"],
        risk=remediation["risk"]
    )

    remediation["remediation_id"] = remediation_id

    return remediation