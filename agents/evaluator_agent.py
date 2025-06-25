# agents/evaluator_agent.py

def evaluate_candidate(match_score, fairness_score, ethics_flags, missing_keywords):
    explanation = []

    # Assign weights (customizable)
    final_score = (match_score * 0.7) + (fairness_score * 0.3)

    if ethics_flags["gap_year_detected"]:
        explanation.append("Gap years flagged")

    if ethics_flags["gender_bias_possible"]:
        explanation.append("Gender may have been inferred")

    if len(missing_keywords) >= 5:
        explanation.append(f"{len(missing_keywords)} important skills missing")

    # Decision logic
    if final_score >= 0.85:
        decision = "✅ Shortlist"
    elif final_score >= 0.6:
        decision = "🟡 Review Manually"
    else:
        decision = "❌ Reject"

    return {
        "final_score": round(final_score, 2),
        "decision": decision,
        "explanation": explanation or ["No major issues found"]
    }
