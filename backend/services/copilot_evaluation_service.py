from backend.services.reliability_copilot_service import investigate_incident
from backend.tests.copilot_evaluation_cases import EVALUATION_CASES


def evaluate_case(case: dict) -> dict:
    result = investigate_incident(case["incident_id"])

    response_text = (
        f"{result.get('summary', '')} "
        f"{result.get('root_cause', '')} "
        f"{result.get('recommended_action', '')}"
    ).lower()

    matched_keywords = [
        keyword
        for keyword in case["expected_root_cause_keywords"]
        if keyword.lower() in response_text
    ]

    keyword_score = (
        len(matched_keywords)
        / len(case["expected_root_cause_keywords"])
    )

    confidence_match = (
        result.get("confidence") == case["expected_confidence"]
    )

    return {
        "case": case["name"],
        "keyword_score": keyword_score,
        "matched_keywords": matched_keywords,
        "confidence_match": confidence_match,
        "result": result,
    }


def run_evaluation() -> None:
    print("=== COPILOT EVALUATION ===")

    total_keyword_score = 0
    confidence_matches = 0
    total_cases = len(EVALUATION_CASES)

    for case in EVALUATION_CASES:
        evaluation = evaluate_case(case)

        print("AI Result:")
        print(evaluation["result"])

        total_keyword_score += evaluation["keyword_score"]

        if evaluation["confidence_match"]:
            confidence_matches += 1

        print(f"\nCase: {evaluation['case']}")
        print(
            f"Keyword score: "
            f"{evaluation['keyword_score']:.2f}"
        )
        print(
            f"Confidence match: "
            f"{evaluation['confidence_match']}"
        )
        print(
            f"Matched keywords: "
            f"{evaluation['matched_keywords']}"
        )

    average_keyword_score = (
        total_keyword_score / total_cases
    )

    confidence_accuracy = (
        confidence_matches / total_cases
    )

    print("\n=== OVERALL EVALUATION ===")
    print(
        f"Average keyword score: "
        f"{average_keyword_score:.2f}"
    )
    print(
        f"Confidence accuracy: "
        f"{confidence_accuracy:.2%}"
    )
    print(
        f"Cases evaluated: "
        f"{total_cases}"
    )


if __name__ == "__main__":
    run_evaluation()