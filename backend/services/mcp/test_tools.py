
from backend.services.mcp.tools import (
    get_pipeline_runs,
    get_data_quality_results,
)

from backend.services.mcp.tools import (
    get_anomaly_results,
    get_remediation_status,
)

from backend.services.mcp.tools import get_incidents

def test_pipeline_runs_limit_validation():
    result = get_pipeline_runs(limit=0)
    assert "error" in result


def test_quality_results_limit_validation():
    result = get_data_quality_results(limit=101)
    assert "error" in result


def test_pipeline_runs_returns_expected_shape():
    result = get_pipeline_runs(limit=5)

    assert "count" in result
    assert "runs" in result
    assert isinstance(result["runs"], list)


def test_quality_results_returns_expected_shape():
    result = get_data_quality_results(limit=5)

    assert "count" in result
    assert "results" in result
    assert isinstance(result["results"], list)


def test_pipeline_runs_returns_expected_structure():
    result = get_pipeline_runs(limit=5)

    assert "count" in result
    assert "runs" in result
    assert isinstance(result["count"], int)
    assert isinstance(result["runs"], list)
    assert result["count"] == len(result["runs"])


def test_data_quality_results_returns_expected_structure():
    result = get_data_quality_results(limit=5)

    assert "count" in result
    assert "results" in result
    assert isinstance(result["count"], int)
    assert isinstance(result["results"], list)
    assert result["count"] == len(result["results"])


from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError


def test_pipeline_runs_handles_database_error():
    with patch(
        "backend.services.mcp.tools.SessionLocal"
    ) as mock_session_local:
        mock_db = mock_session_local.return_value
        mock_db.execute.side_effect = SQLAlchemyError(
            "Simulated database failure"
        )

        result = get_pipeline_runs(limit=5)

        assert result == {"error": "Database query failed"}
        mock_db.close.assert_called_once()


def test_data_quality_results_handles_database_error():
    with patch(
        "backend.services.mcp.tools.SessionLocal"
    ) as mock_session_local:
        mock_db = mock_session_local.return_value
        mock_db.execute.side_effect = SQLAlchemyError(
            "Simulated database failure"
        )

        result = get_data_quality_results(limit=5)

        assert result == {"error": "Database query failed"}
        mock_db.close.assert_called_once()


def test_pipeline_runs_accepts_minimum_limit():
    result = get_pipeline_runs(limit=1)
    assert "error" not in result
    assert result["count"] <= 1


def test_pipeline_runs_accepts_maximum_limit():
    result = get_pipeline_runs(limit=100)
    assert "error" not in result
    assert result["count"] <= 100


def test_data_quality_results_accepts_minimum_limit():
    result = get_data_quality_results(limit=1)
    assert "error" not in result
    assert result["count"] <= 1


def test_data_quality_results_accepts_maximum_limit():
    result = get_data_quality_results(limit=100)
    assert "error" not in result
    assert result["count"] <= 100


def test_pipeline_runs_dataset_filter():
    result = get_pipeline_runs(dataset="__nonexistent_dataset__", limit=5)

    assert "error" not in result
    assert result["count"] == 0
    assert result["runs"] == []


def test_data_quality_results_dataset_filter():
    result = get_data_quality_results(
        dataset="__nonexistent_dataset__",
        limit=5,
    )

    assert "error" not in result
    assert result["count"] == 0
    assert result["results"] == []


def test_data_quality_results_status_filter():
    result = get_data_quality_results(
        check_status="__nonexistent_status__",
        limit=5,
    )

    assert "error" not in result
    assert result["count"] == 0
    assert result["results"] == []


def test_get_incidents_returns_expected_structure():
    result = get_incidents(limit=20)

    assert "count" in result
    assert "incidents" in result
    assert isinstance(result["incidents"], list)

    if result["incidents"]:
        incident = result["incidents"][0]
        assert "incident_id" in incident
        assert "dataset" in incident
        assert "severity" in incident
        assert "status" in incident
        assert "detected_at" in incident
        assert "resolved_at" in incident


def test_get_incidents_rejects_invalid_limit():
    assert get_incidents(limit=0) == {
        "error": "limit must be between 1 and 100"
    }
    assert get_incidents(limit=101) == {
        "error": "limit must be between 1 and 100"
    }


def test_get_incidents_dataset_filter():
    result = get_incidents(dataset="retail", limit=20)

    assert "error" not in result
    assert all(
        incident["dataset"] == "retail"
        for incident in result["incidents"]
    )


def test_get_incidents_status_filter():
    result = get_incidents(status="OPEN", limit=20)

    assert "error" not in result
    assert all(
        incident["status"] == "OPEN"
        for incident in result["incidents"]
    )


def test_anomaly_results_rejects_invalid_limit():
    assert get_anomaly_results(limit=0) == {
        "error": "limit must be between 1 and 100"
    }
    assert get_anomaly_results(limit=101) == {
        "error": "limit must be between 1 and 100"
    }


def test_anomaly_results_returns_expected_structure():
    result = get_anomaly_results(limit=5)

    assert "error" not in result
    assert isinstance(result["count"], int)
    assert isinstance(result["anomalies"], list)
    assert result["count"] == len(result["anomalies"])


def test_anomaly_results_store_filter():
    result = get_anomaly_results(
        store_id="__nonexistent_store__",
        limit=5,
    )

    assert "error" not in result
    assert result["count"] == 0
    assert result["anomalies"] == []


def test_anomaly_results_status_filter():
    result = get_anomaly_results(
        anomaly_status="__nonexistent_status__",
        limit=5,
    )

    assert "error" not in result
    assert result["count"] == 0
    assert result["anomalies"] == []


def test_remediation_status_rejects_invalid_id():
    assert get_remediation_status(0) == {
        "error": "remediation_id must be a positive integer"
    }


def test_remediation_status_returns_not_found_for_missing_record():
    result = get_remediation_status(2_000_000_000)

    assert result == {"error": "Remediation not found"}


def test_anomaly_results_handles_database_error():
    with patch(
        "backend.services.mcp.tools.SessionLocal"
    ) as mock_session_local:
        mock_db = mock_session_local.return_value
        mock_db.execute.side_effect = SQLAlchemyError(
            "Simulated database failure"
        )

        result = get_anomaly_results(limit=5)

        assert result == {"error": "Database query failed"}
        mock_db.close.assert_called_once()


def test_remediation_status_handles_database_error():
    with patch(
        "backend.services.mcp.tools.SessionLocal"
    ) as mock_session_local:
        mock_db = mock_session_local.return_value
        mock_db.execute.side_effect = SQLAlchemyError(
            "Simulated database failure"
        )

        result = get_remediation_status(1)

        assert result == {"error": "Database query failed"}
        mock_db.close.assert_called_once()
