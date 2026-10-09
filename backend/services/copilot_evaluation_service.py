
from backend.services.reliability.graph import run_reliability_graph
from backend.tests.copilot_evaluation_cases import EVALUATION_CASES


def evaluate_case(case: dict) -> dict:
    graph_result = run_reliability_graph(case["incident_id"])
    result = graph_result.get("analysis", {})

    response_text = (
        f"{result.get('summary', '')} "
        f"{result.get('root_cause', '')} "
        f"{result.get('recommended_action', '')}"
    ).lower()

    expected_keywords = case["expected_root_cause_keywords"]

    matched_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in response_text
    ]

    keyword_score = (
        len(matched_keywords) / len(expected_keywords)
        if expected_keywords
        else 1.0
    )

    incident_detected = bool(result.get("summary", "").strip())

    root_cause_confirmed = (
        result.get("evidence_sufficient") is True
        and bool(result.get("root_cause", "").strip())
    )

    expected_incident_detected = case["incident_should_be_detected"]
    expected_root_cause_confirmed = case["root_cause_should_be_confirmed"]

    incident_detection_match = (
        incident_detected == expected_incident_detected
    )

    root_cause_confirmation_match = (
        root_cause_confirmed == expected_root_cause_confirmed
    )

    return {
        "case": case["name"],
        "keyword_score": keyword_score,
        "matched_keywords": matched_keywords,
        "incident_detected": incident_detected,
        "incident_detection_match": incident_detection_match,
        "root_cause_confirmed": root_cause_confirmed,
        "root_cause_confirmation_match": root_cause_confirmation_match,
        "result": result,
    }


def run_evaluation() -> None:
    print("=== COPILOT EVALUATION ===")

    total_keyword_score = 0.0
    incident_detection_matches = 0
    root_cause_confirmation_matches = 0
    total_cases = len(EVALUATION_CASES)

    for case in EVALUATION_CASES:
        evaluation = evaluate_case(case)

        total_keyword_score += evaluation["keyword_score"]
        incident_detection_matches += int(
            evaluation["incident_detection_match"]
        )
        root_cause_confirmation_matches += int(
            evaluation["root_cause_confirmation_match"]
        )

        print(f"\nCase: {evaluation['case']}")
        print(f"Keyword score: {evaluation['keyword_score']:.2f}")
        print(f"Matched keywords: {evaluation['matched_keywords']}")
        print(f"Incident detected: {evaluation['incident_detected']}")
        print(
            "Incident detection match: "
            f"{evaluation['incident_detection_match']}"
        )
        print(
            "Root cause confirmed: "
            f"{evaluation['root_cause_confirmed']}"
        )
        print(
            "Root cause confirmation match: "
            f"{evaluation['root_cause_confirmation_match']}"
        )

    if total_cases == 0:
        print("\nNo evaluation cases configured.")
        return

    print("\n=== OVERALL EVALUATION ===")
    print(f"Average keyword score: {total_keyword_score / total_cases:.2f}")
    print(
        "Incident detection accuracy: "
        f"{incident_detection_matches / total_cases:.2%}"
    )
    print(
        "Root-cause confirmation accuracy: "
        f"{root_cause_confirmation_matches / total_cases:.2%}"
    )
    print(f"Cases evaluated: {total_cases}")


if __name__ == "__main__":
    run_evaluation()
