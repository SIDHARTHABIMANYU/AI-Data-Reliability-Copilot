from backend.services.evidence_service import collect_incident_evidence
from backend.services.reliability_rag_service import retrieve_reliability_context


def build_copilot_context(incident_id: int) -> dict:
    evidence = collect_incident_evidence(incident_id)

    incident = evidence.get("incident", {})

    query = (
        f"How should we investigate and handle this incident? "
        f"Dataset: {incident.get('dataset')}. "
        f"Incident type: {incident.get('incident_type')}. "
        f"Description: {incident.get('description')}."
    )

    reliability_context = retrieve_reliability_context(query)

    return {
        "incident_evidence": evidence,
        "reliability_context": reliability_context,
    }

if __name__ == "__main__":
    context = build_copilot_context(1)

    print("\n=== INCIDENT EVIDENCE ===")
    print(context["incident_evidence"])

    print("\n=== RELIABILITY KNOWLEDGE ===")
    print(context["reliability_context"])