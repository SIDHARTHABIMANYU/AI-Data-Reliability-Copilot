from backend.services import reliability_copilot_service


def test_investigate_incident(monkeypatch):
    fake_context = {
        "incident_evidence": {
            "incident_id": 1,
            "issue_type": "schema_mismatch",
            "details": "sales_amount column is missing",
        },
        "reliability_context": [
            "Schema changes must be reviewed before mapping fields."
        ],
    }

    fake_response = {
        "summary": "Sales pipeline schema changed.",
        "root_cause": "Upstream column renamed.",
        "evidence": [
            "sales_amount column is missing."
        ],
        "impact": [
            "Daily revenue pipeline is affected."
        ],
        "recommended_action": (
            "Confirm the new field meaning with the upstream provider."
        ),
        "confidence": "HIGH",
    }

    class FakeLLMResponse:
        content = str(fake_response).replace("'", '"')

    monkeypatch.setattr(
        reliability_copilot_service,
        "build_copilot_context",
        lambda incident_id: fake_context,
    )

    class FakeLLM:
        def invoke(self, prompt):
            return FakeLLMResponse()

    monkeypatch.setattr(
        reliability_copilot_service,
        "llm",
        FakeLLM(),
    )

    result = reliability_copilot_service.investigate_incident(1)

    assert result["summary"] == "Sales pipeline schema changed."
    assert result["root_cause"] == "Upstream column renamed."
    assert result["confidence"] == "HIGH"

    assert "sales_amount column is missing." in result["evidence"]
    assert "Daily revenue pipeline is affected." in result["impact"]