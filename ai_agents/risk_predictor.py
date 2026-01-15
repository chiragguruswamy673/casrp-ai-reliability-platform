from ai_agents.prompts.risk_prompt import build_risk_prompt

def predict_risk(system_snapshot: dict) -> dict:
    prompt = build_risk_prompt(system_snapshot)

    # 🔴 Simulated LLM response (for now)
    if system_snapshot["recent_failures"]:
        risk = 0.6
        explanation = "Recent test failures indicate instability."
    elif system_snapshot["db_schema_version"]:
        risk = 0.5
        explanation = "Database schema change without validation increases risk."
    elif system_snapshot["services"]:
        risk = 0.3
        explanation = "Service code changed; regression risk present."
    else:
        risk = 0.1
        explanation = "System stable with no recent changes."

    return {
        "risk_score": risk,
        "explanation": explanation,
        "prompt_used": prompt
    }
