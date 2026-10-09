from typing import Any

from langgraph.graph import StateGraph, START, END

from backend.services.reliability.state import ReliabilityState

from backend.services.reliability.nodes import (
    collect_evidence_node,
    retrieve_rag_node,
    analyze_incident_node,
    validate_evidence_node,
    build_impact_node,
    build_recommendation_node,
)


def route_after_validation(
    state: ReliabilityState,
) -> str:
    """
    Decide whether the investigation has enough
    evidence to continue.
    """

    if state.get("evidence_sufficient", False):
        return "sufficient"

    return "insufficient"


workflow = StateGraph(ReliabilityState)


workflow.add_node(
    "collect_evidence",
    collect_evidence_node,
)

workflow.add_node(
    "retrieve_rag",
    retrieve_rag_node,
)

workflow.add_node(
    "analyze_incident",
    analyze_incident_node,
)

workflow.add_node(
    "validate_evidence",
    validate_evidence_node,
)

workflow.add_node(
    "build_impact",
    build_impact_node,
)

workflow.add_node(
    "build_recommendation",
    build_recommendation_node,
)


workflow.add_edge(
    START,
    "collect_evidence",
)

workflow.add_edge(
    "collect_evidence",
    "retrieve_rag",
)

workflow.add_edge(
    "retrieve_rag",
    "analyze_incident",
)

workflow.add_edge(
    "analyze_incident",
    "validate_evidence",
)


workflow.add_conditional_edges(
    "validate_evidence",
    route_after_validation,
    {
        "sufficient": "build_impact",
        "insufficient": END,
    },
)


workflow.add_edge(
    "build_impact",
    "build_recommendation",
)

workflow.add_edge(
    "build_recommendation",
    END,
)


reliability_graph = workflow.compile()


def run_reliability_graph(
    incident_id: int,
) -> dict[str, Any]:
    """
    Run the complete reliability investigation workflow.
    """

    initial_state: ReliabilityState = {
        "incident_id": incident_id
    }

    result = reliability_graph.invoke(
        initial_state
    )

    return result

if __name__ == "__main__":
    result = run_reliability_graph(1)

    print("\n===== RELIABILITY GRAPH RESULT =====")
    print(result)