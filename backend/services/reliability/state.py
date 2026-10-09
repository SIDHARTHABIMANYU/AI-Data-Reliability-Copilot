from typing import Any, TypedDict


class ReliabilityState(TypedDict, total=False):
    incident_id: int

    evidence: dict[str, Any]
    rag_context: list[dict[str, Any]]

    analysis: dict[str, Any]

    evidence_sufficient: bool

    impact: list[str]
    recommendation: str
    confidence: str