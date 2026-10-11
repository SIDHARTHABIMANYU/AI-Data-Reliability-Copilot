from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from backend.services.remediation_approval_service import (
    approve_remediation,
    reject_remediation,
)


@pytest.fixture
def mock_db():
    with patch(
        "backend.services.remediation_approval_service.SessionLocal"
    ) as session_factory:
        db = MagicMock()
        session_factory.return_value = db
        yield db


def make_remediation(status="PENDING"):
    remediation = MagicMock()
    remediation.remediation_id = 7
    remediation.incident_id = 12
    remediation.proposed_change = "Fix invalid revenue records"
    remediation.risk = "LOW"
    remediation.status = status
    remediation.approved_by = None
    remediation.approved_at = None
    remediation.rejected_by = None
    remediation.rejected_at = None
    remediation.created_at = datetime(2026, 10, 11, 10, 0, 0)
    return remediation


def configure_lookup(mock_db, remediation):
    query = mock_db.query.return_value
    query.filter.return_value = query
    query.with_for_update.return_value = query
    query.first.return_value = remediation


def test_approve_pending_remediation_sets_approval_audit(mock_db):
    remediation = make_remediation()
    configure_lookup(mock_db, remediation)

    result = approve_remediation(7, "reviewer")

    assert result["status"] == "APPROVED"
    assert result["approved_by"] == "reviewer"
    assert isinstance(result["approved_at"], datetime)
    assert remediation.rejected_by is None
    assert remediation.rejected_at is None
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_reject_pending_remediation_sets_rejection_audit(mock_db):
    remediation = make_remediation()
    configure_lookup(mock_db, remediation)

    result = reject_remediation(7, "reviewer")

    assert result["status"] == "REJECTED"
    assert result["rejected_by"] == "reviewer"
    assert isinstance(result["rejected_at"], datetime)
    assert remediation.approved_by is None
    assert remediation.approved_at is None
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


@pytest.mark.parametrize(
    ("function", "existing_status"),
    [
        (approve_remediation, "APPROVED"),
        (approve_remediation, "REJECTED"),
        (reject_remediation, "APPROVED"),
        (reject_remediation, "REJECTED"),
    ],
)
def test_cannot_decide_already_decided_remediation(
    mock_db, function, existing_status
):
    remediation = make_remediation(status=existing_status)
    configure_lookup(mock_db, remediation)

    result = function(7, "reviewer")

    assert "error" in result
    assert result["error"] == f"Remediation is already {existing_status}"
    mock_db.commit.assert_not_called()
    mock_db.close.assert_called_once()


@pytest.mark.parametrize(
    "function",
    [approve_remediation, reject_remediation],
)
def test_missing_remediation_returns_error(mock_db, function):
    configure_lookup(mock_db, None)

    result = function(999999, "reviewer")

    assert result == {"error": "Remediation not found"}
    mock_db.commit.assert_not_called()
    mock_db.close.assert_called_once()


def test_approval_database_failure_rolls_back_and_closes(mock_db):
    remediation = make_remediation()
    configure_lookup(mock_db, remediation)
    mock_db.commit.side_effect = RuntimeError("database failure")

    with pytest.raises(RuntimeError, match="database failure"):
        approve_remediation(7, "reviewer")

    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()


def test_rejection_database_failure_rolls_back_and_closes(mock_db):
    remediation = make_remediation()
    configure_lookup(mock_db, remediation)
    mock_db.commit.side_effect = RuntimeError("database failure")

    with pytest.raises(RuntimeError, match="database failure"):
        reject_remediation(7, "reviewer")

    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()
