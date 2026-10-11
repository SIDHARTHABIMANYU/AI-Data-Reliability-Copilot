from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


@patch("backend.routers.remediation_approval.approve_remediation")
def test_approve_pending_remediation(mock_approve):
    mock_approve.return_value = {
        "remediation_id": 1,
        "incident_id": 10,
        "status": "APPROVED",
        "approved_by": "tester",
        "approved_at": "2026-10-11T10:00:00",
    }

    response = client.post(
        "/remediations/1/approve",
        json={"approved_by": "tester"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"
    mock_approve.assert_called_once_with(
        remediation_id=1,
        approved_by="tester",
    )


@patch("backend.routers.remediation_approval.reject_remediation")
def test_reject_pending_remediation(mock_reject):
    mock_reject.return_value = {
        "remediation_id": 1,
        "incident_id": 10,
        "status": "REJECTED",
        "rejected_by": "tester",
        "rejected_at": "2026-10-11T10:00:00",
    }

    response = client.post(
        "/remediations/1/reject",
        json={"approved_by": "tester"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "REJECTED"
    assert "rejected_by" in response.json()
    mock_reject.assert_called_once_with(
        remediation_id=1,
        rejected_by="tester",
    )


@pytest.mark.parametrize(
    "endpoint",
    [
        "/remediations/0/approve",
        "/remediations/0/reject",
    ],
)
def test_remediation_decision_rejects_nonpositive_id(endpoint):
    response = client.post(
        endpoint,
        json={"approved_by": "tester"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "endpoint",
    [
        "/remediations/1/approve",
        "/remediations/1/reject",
    ],
)
def test_remediation_decision_rejects_blank_approver(endpoint):
    response = client.post(
        endpoint,
        json={"approved_by": "   "},
    )

    assert response.status_code == 422


@patch("backend.routers.remediation_approval.approve_remediation")
def test_approve_missing_remediation_returns_404(mock_approve):
    mock_approve.return_value = {"error": "Remediation not found"}

    response = client.post(
        "/remediations/999999/approve",
        json={"approved_by": "tester"},
    )

    assert response.status_code == 404


@patch("backend.routers.remediation_approval.reject_remediation")
def test_reject_already_decided_remediation_returns_409(mock_reject):
    mock_reject.return_value = {
        "error": "Remediation is already APPROVED"
    }

    response = client.post(
        "/remediations/1/reject",
        json={"approved_by": "tester"},
    )

    assert response.status_code == 409
