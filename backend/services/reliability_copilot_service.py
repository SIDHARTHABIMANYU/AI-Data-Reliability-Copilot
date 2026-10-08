import json

from langchain_aws import ChatBedrockConverse

from backend.config.settings import settings
from backend.services.copilot_context_service import build_copilot_context


llm = ChatBedrockConverse(
    model=settings.BEDROCK_MODEL_ID,
    region_name=settings.AWS_REGION,
    max_tokens=1000,
    temperature=0.2,
)


SYSTEM_PROMPT = """
You are an AI Data Reliability Copilot for a retail data platform.

Your job is to investigate data incidents using only the provided
incident evidence and reliability knowledge.

You must:

1. Identify the most likely root cause.
2. Explain the evidence supporting the conclusion.
3. Identify affected business metrics or downstream systems.
4. Recommend the safest next action.
5. Never assume that a renamed field has the same business meaning.
6. Never invent missing evidence.
7. Clearly state when the evidence is insufficient.
8. Treat remediation as a recommendation requiring human review.

Return ONLY valid JSON using this structure:

{
    "summary": "Short explanation of the incident.",
    "root_cause": "Most likely root cause.",
    "evidence": [
        "Evidence supporting the conclusion."
    ],
    "impact": [
        "Affected business metrics or downstream systems."
    ],
    "recommended_action": "Safest recommended next action.",
    "confidence": "HIGH"
}
"""


def investigate_incident(incident_id: int) -> dict:
    context = build_copilot_context(incident_id)

    incident_evidence = context["incident_evidence"]
    reliability_context = context["reliability_context"]

    prompt = f"""
{SYSTEM_PROMPT}

INCIDENT EVIDENCE:
{incident_evidence}

RELIABILITY KNOWLEDGE:
{reliability_context}

Investigate incident {incident_id}.
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

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)


if __name__ == "__main__":
    result = investigate_incident(1)

    print("\n=== AI RELIABILITY COPILOT ===")
    print(json.dumps(result, indent=4))