import pandas as pd

from backend.services import anomaly_evaluation_service


def test_evaluate_anomaly_detection(tmp_path, monkeypatch, capsys):
    statistical_file = tmp_path / "statistical_results.csv"
    ml_file = tmp_path / "ml_results.csv"

    statistical_df = pd.DataFrame(
        {
            "transaction_date": [
                "2026-02-01",
                "2026-02-02",
                "2026-02-03",
            ],
            "store_id": [
                "STORE01",
                "STORE02",
                "STORE03",
            ],
            "revenue_z_score": [
                1.2,
                3.5,
                -4.0,
            ],
            "anomaly_status": [
                "NORMAL",
                "ANOMALY",
                "ANOMALY",
            ],
        }
    )

    ml_df = pd.DataFrame(
        {
            "transaction_date": [
                "2026-02-02",
                "2026-02-04",
            ],
            "store_id": [
                "STORE02",
                "STORE04",
            ],
            "ml_anomaly_status": [
                "ANOMALY",
                "ANOMALY",
            ],
        }
    )

    statistical_df.to_csv(statistical_file, index=False)
    ml_df.to_csv(ml_file, index=False)

    monkeypatch.setattr(
        anomaly_evaluation_service,
        "STATISTICAL_FILE",
        statistical_file,
    )

    monkeypatch.setattr(
        anomaly_evaluation_service,
        "ML_FILE",
        ml_file,
    )

    anomaly_evaluation_service.evaluate_anomaly_detection()

    output = capsys.readouterr().out

    assert "Evaluated rows: 3" in output
    assert "Anomalies: 2" in output

    assert "Evaluated rows: 2" in output
    assert "Anomalies: 2" in output

    assert "Both detected: 1" in output
    assert "ML only: 1" in output
    assert "Statistical only: 1" in output