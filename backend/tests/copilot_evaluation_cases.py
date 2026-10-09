EVALUATION_CASES = [
    {
        "name": "schema_change",
        "incident_id": 1,
        "expected_root_cause_keywords": [
            "schema",
            "sales_amount",
            "net_amount",
        ],
        "incident_should_be_detected": True,
        "root_cause_should_be_confirmed": False,
    },
    {
        "name": "duplicate_transactions",
        "incident_id": 2,
        "expected_root_cause_keywords": [
            "duplicate",
            "transaction",
        ],
        "incident_should_be_detected": True,
        "root_cause_should_be_confirmed": False,
    },
    {
        "name": "missing_data",
        "incident_id": 3,
        "expected_root_cause_keywords": [
            "missing",
            "file",
        ],
        "incident_should_be_detected": True,
        "root_cause_should_be_confirmed": False,
    },
    {
        "name": "revenue_anomaly",
        "incident_id": 6,
        "expected_root_cause_keywords": [
            "anomaly",
            "revenue",
        ],
        "incident_should_be_detected": True,
        "root_cause_should_be_confirmed": False,
    },
]