import pandas as pd

from backend.services import ml_anomaly_service


def test_detect_ml_anomalies(tmp_path, monkeypatch):
    input_file = tmp_path / "features.csv"
    output_file = tmp_path / "ml_results.csv"

    rows = []

    for i in range(20):
        rows.append(
            {
                "total_revenue": 100 + i,
                "total_transactions": 50 + i,
                "total_quantity": 100 + i,
                "revenue_change_pct": 0.01 * i,
                "transaction_change_pct": 0.01 * i,
                "quantity_change_pct": 0.01 * i,
                "revenue_deviation_pct": 0.01 * i,
            }
        )

    df = pd.DataFrame(rows)
    df.loc[0, "total_revenue"] = 10000

    df.to_csv(input_file, index=False)

    monkeypatch.setattr(
        ml_anomaly_service,
        "INPUT_FILE",
        input_file,
    )

    monkeypatch.setattr(
        ml_anomaly_service,
        "OUTPUT_FILE",
        output_file,
    )

    ml_anomaly_service.detect_ml_anomalies()

    result = pd.read_csv(output_file)

    assert len(result) == 20

    assert "ml_prediction" in result.columns
    assert "ml_anomaly_score" in result.columns
    assert "ml_anomaly_status" in result.columns

    assert set(result["ml_prediction"].unique()).issubset({1, -1})

    assert set(result["ml_anomaly_status"].unique()).issubset(
        {"NORMAL", "ANOMALY"}
    )

    assert result["detection_method"].eq(
        "ISOLATION_FOREST"
    ).all()