EVALUATION_CASES = [
    {
        "name": "schema_change",
        "incident_id": 1,
        "expected_root_cause_keywords": [
            "schema",
            "sales_amount",
            "net_amount",
        ],
        "expected_confidence": "HIGH",
    },
    {
        "name": "duplicate_transactions",
        "incident_id": 2,
        "expected_root_cause_keywords": [
            "duplicate",
            "transaction",
        ],
        "expected_confidence": "MEDIUM",
    },
    {
        "name": "missing_data",
        "incident_id": 3,
        "expected_root_cause_keywords": [
            "missing",
            "file",
        ],
        "expected_confidence": "HIGH",
    },
    {
        "name": "revenue_anomaly",
        "incident_id": 6,
        "expected_root_cause_keywords": [
            "anomaly",
            "revenue",
        ],
        "expected_confidence": "MEDIUM",
    },
]