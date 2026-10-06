from backend.services.data_quality_service import record_quality_result


record_quality_result(
    dataset="sales",
    file_name="sales_2026-03-31.csv",
    check_name="schema_validation",
    check_status="PASS",
    expected_value="6 columns",
    actual_value="6 columns",
)