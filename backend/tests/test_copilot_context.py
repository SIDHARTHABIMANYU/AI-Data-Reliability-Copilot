
from backend.services.reliability.nodes import (
    retrieve_rag_node,
)


def test_retrieve_rag_context(monkeypatch):
    fake_evidence = {
        "incident": {
            "dataset": "sales",
            "incident_type": "SCHEMA_CHANGE",
            "description": "sales_amount column is missing",
        }
    }

    fake_reliability_context = (
        "Schema changes should be reviewed before mapping fields."
    )

    captured_query = {}

    def fake_retrieve_reliability_context(query):
        captured_query["query"] = query
        return fake_reliability_context

    from backend.services.reliability import nodes

    monkeypatch.setattr(
        nodes,
        "retrieve_reliability_context",
        fake_retrieve_reliability_context,
    )

    result = retrieve_rag_node({"evidence": fake_evidence})

    assert result["rag_context"] == fake_reliability_context
    assert "Dataset: sales" in captured_query["query"]
    assert "Incident type: SCHEMA_CHANGE" in captured_query["query"]
    assert "sales_amount column is missing" in captured_query["query"]
