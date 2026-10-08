from backend.services import copilot_context_service


def test_build_copilot_context(monkeypatch):
    fake_evidence = {
        "incident": {
            "dataset": "sales",
            "incident_type": "schema_mismatch",
            "description": "sales_amount column is missing",
        },
        "pipeline_run": {
            "run_id": 274,
        },
    }

    fake_reliability_context = [
        "Schema changes should be reviewed before applying field mappings.",
        "Confirm business meaning before repairing renamed columns.",
    ]

    captured_query = {}

    def fake_collect_incident_evidence(incident_id):
        assert incident_id == 1
        return fake_evidence

    def fake_retrieve_reliability_context(query):
        captured_query["query"] = query
        return fake_reliability_context

    monkeypatch.setattr(
        copilot_context_service,
        "collect_incident_evidence",
        fake_collect_incident_evidence,
    )

    monkeypatch.setattr(
        copilot_context_service,
        "retrieve_reliability_context",
        fake_retrieve_reliability_context,
    )

    result = copilot_context_service.build_copilot_context(1)

    assert result["incident_evidence"] == fake_evidence
    assert result["reliability_context"] == fake_reliability_context

    assert "Dataset: sales" in captured_query["query"]
    assert "Incident type: schema_mismatch" in captured_query["query"]
    assert "sales_amount column is missing" in captured_query["query"]