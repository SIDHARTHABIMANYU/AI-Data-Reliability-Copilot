import json
from typing import Any

from langchain_aws import ChatBedrockConverse

from backend.config.settings import settings
from backend.services.evidence_service import collect_incident_evidence
from backend.services.reliability_rag_service import (
    retrieve_reliability_context,
)

from backend.services.reliability.state import ReliabilityState


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
9. Determine whether the available evidence is sufficient
   to support the root-cause conclusion.
10. Return "evidence_sufficient" as a JSON boolean:
    true only when the evidence directly supports the conclusion;
    false when key facts are missing or the cause remains uncertain.

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
    "confidence": "HIGH",
    "evidence_sufficient": false
}
"""


def collect_evidence_node(
    state: ReliabilityState,
) -> dict[str, Any]:
    """
    Collect factual incident evidence from the existing
    evidence service.
    """

    incident_id = state["incident_id"]

    evidence = collect_incident_evidence(
        incident_id
    )

    return {
        "evidence": evidence
    }


def retrieve_rag_node(
    state: ReliabilityState,
) -> dict[str, Any]:
    """
    Retrieve reliability knowledge using the incident
    information collected by the evidence node.
    """

    evidence = state.get("evidence", {})

    incident = evidence.get(
        "incident",
        {}
    )

    query = (
        "How should we investigate and handle this incident? "
        f"Dataset: {incident.get('dataset')}. "
        f"Incident type: {incident.get('incident_type')}. "
        f"Description: {incident.get('description')}."
    )

    reliability_context = retrieve_reliability_context(
        query
    )

    return {
        "rag_context": reliability_context
    }


def analyze_incident_node(
    state: ReliabilityState,
) -> dict[str, Any]:
    """
    Analyze the incident using the collected evidence
    and retrieved reliability knowledge.
    """

    incident_id = state["incident_id"]

    evidence = state.get(
        "evidence",
        {}
    )

    rag_context = state.get(
        "rag_context",
        ""
    )

    prompt = f"""
{SYSTEM_PROMPT}

INCIDENT EVIDENCE:
{json.dumps(evidence, default=str, indent=2)}

RELIABILITY KNOWLEDGE:
{rag_context}

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
        content = content.replace(
            "```json",
            ""
        )
        content = content.replace(
            "```",
            ""
        )
        content = content.strip()

    analysis = json.loads(content)

    return {
        "analysis": analysis
    }


def validate_evidence_node(
    state: ReliabilityState,
) -> dict[str, Any]:
    """
    Validate whether the collected evidence supports the
    incident diagnosis. Incident confirmation does not
    automatically prove the underlying root cause.
    """

    analysis = state.get("analysis", {})
    incident_evidence = state.get("evidence", {})

    incident = incident_evidence.get("incident", {})
    pipeline_run = incident_evidence.get("pipeline_run")
    quality_results = incident_evidence.get(
        "quality_results", []
    )

    incident_exists = bool(incident.get("incident_id"))
    incident_type = incident.get("incident_type", "")

    failed_quality_check = any(
        result.get("check_status") == "FAIL"
        for result in quality_results
    )

    failed_pipeline = (
        isinstance(pipeline_run, dict)
        and pipeline_run.get("status") == "FAILED"
    )

    # Confirm the incident using evidence appropriate to its type.
    if incident_type == "SCHEMA_CHANGE":
        incident_confirmed = (
            failed_quality_check or failed_pipeline
        )
    elif incident_type == "DUPLICATE_TRANSACTIONS":
        incident_confirmed = (
            "duplicate" in incident.get("description", "").lower()
        )
    elif incident_type == "MISSING_DATA":
        incident_confirmed = (
            "missing" in incident.get("description", "").lower()
            or "not received" in incident.get(
                "description", ""
            ).lower()
        )
    elif incident_type == "ANOMALY":
        incident_confirmed = (
            "anomaly" in incident.get("description", "").lower()
            and "z-score" in incident.get("description", "").lower()
        )
    else:
        incident_confirmed = False

    root_cause = analysis.get("root_cause", "").strip()
    evidence_items = analysis.get("evidence", [])

    model_says_sufficient = (
        analysis.get("evidence_sufficient") is True
    )

    evidence_sufficient = (
        incident_exists
        and incident_confirmed
        and bool(root_cause)
        and bool(evidence_items)
        and model_says_sufficient
    )

    return {
        "evidence_sufficient": evidence_sufficient
    }


def build_impact_node(
    state: ReliabilityState,
) -> dict[str, Any]:
    """
    Extract the business impact identified by the
    investigation.
    """

    analysis = state.get(
        "analysis",
        {}
    )

    return {
        "impact": analysis.get(
            "impact",
            []
        )
    }


def build_recommendation_node(
    state: ReliabilityState,
) -> dict[str, Any]:
    """
    Extract the recommended action and confidence
    from the investigation.
    """

    analysis = state.get(
        "analysis",
        {}
    )

    return {
        "recommendation": analysis.get(
            "recommended_action",
            ""
        ),
        "confidence": analysis.get(
            "confidence",
            "LOW"
        ),
    }