
from backend.services.reliability.graph import (
    run_reliability_graph,
)


def test_investigate_incident(monkeypatch):
    def fake_collect_evidence(incident_id):
        assert incident_id == 1

        return {
            "incident": {
                "incident_id": 1,
                "incident_type": "SCHEMA_CHANGE",
                "description": "sales_amount column is missing",
            },
            "pipeline_run": {
                "status": "FAILED",
            },
            "quality_results": [
                {"check_status": "FAIL"},
            ],
        }

    def fake_retrieve_context(query):
        return "Schema changes must be reviewed before mapping fields."

    class FakeLLMResponse:
        content = (
            '{"summary": "Sales pipeline schema changed.",'
            '"root_cause": "Upstream column changed.",'
            '"evidence": ["sales_amount column is missing."],'
            '"impact": ["Daily revenue pipeline is affected."],'
            '"recommended_action": "Confirm the new field meaning.",'
            '"confidence": "HIGH",'
            '"evidence_sufficient": true}'
        )

    class FakeLLM:
        def invoke(self, prompt):
            return FakeLLMResponse()

    from backend.services.reliability import nodes

    monkeypatch.setattr(
        nodes,
        "collect_incident_evidence",
        fake_collect_evidence,
    )
    monkeypatch.setattr(
        nodes,
        "retrieve_reliability_context",
        fake_retrieve_context,
    )
    monkeypatch.setattr(nodes, "llm", FakeLLM())

    result = run_reliability_graph(1)

    assert result["analysis"]["summary"] == (
        "Sales pipeline schema changed."
    )
    assert result["analysis"]["root_cause"] == (
        "Upstream column changed."
    )
    assert result["analysis"]["confidence"] == "HIGH"
    assert result["evidence_sufficient"] is True
    assert result["impact"] == [
        "Daily revenue pipeline is affected."
    ]
    assert result["recommendation"] == (
        "Confirm the new field meaning."
    )
