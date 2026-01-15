def summarize_incident(memory_entries):
    if not memory_entries:
        return {
            "summary": "No incidents detected.",
            "severity": "none"
        }

    highest_risk = max(
        memory_entries, key=lambda x: x["risk"]["risk_score"]
    )

    risk_score = highest_risk["risk"]["risk_score"]

    if risk_score >= 0.7:
        severity = "high"
    elif risk_score >= 0.4:
        severity = "medium"
    else:
        severity = "low"

    summary = (
        f"Incident detected with {severity} severity. "
        f"Primary cause: {highest_risk['risk']['explanation']} "
        f"Observed at {highest_risk['timestamp']}."
    )

    return {
        "severity": severity,
        "summary": summary,
        "risk_score": risk_score
    }
