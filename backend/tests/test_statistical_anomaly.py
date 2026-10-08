import pandas as pd

from backend.services import statistical_anomaly_service


def test_detect_statistical_anomalies(tmp_path, monkeypatch):
    input_file = tmp_path / "features.csv"
    output_file = tmp_path / "statistical_results.csv"

    df = pd.DataFrame(
        {
            "total_revenue": [100, 100, 160],
            "revenue_7d_mean": [100, 100, 100],
            "revenue_7d_std": [10, 10, 10],
        }
    )

    df.to_csv(input_file, index=False)

    monkeypatch.setattr(
        statistical_anomaly_service,
        "INPUT_FILE",
        input_file,
    )

    monkeypatch.setattr(
        statistical_anomaly_service,
        "OUTPUT_FILE",
        output_file,
    )

    statistical_anomaly_service.detect_statistical_anomalies()

    result = pd.read_csv(output_file)

    assert result.loc[0, "anomaly_status"] == "NORMAL"
    assert result.loc[1, "anomaly_status"] == "NORMAL"
    assert result.loc[2, "anomaly_status"] == "ANOMALY"

    assert result.loc[2, "revenue_z_score"] == 6.0
    assert result["detection_method"].eq("ROLLING_Z_SCORE").all()