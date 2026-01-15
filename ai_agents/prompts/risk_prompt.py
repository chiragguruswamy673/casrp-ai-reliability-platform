def build_risk_prompt(system_snapshot: dict) -> str:
    return f"""
You are a senior reliability engineer AI.

Analyze the system state below and determine deployment risk.

System State:
- Services changed: {system_snapshot['services']}
- DB schema version: {system_snapshot['db_schema_version']}
- Recent failures: {system_snapshot['recent_failures']}

Rules:
1. Database changes increase risk
2. Repeated failures increase risk
3. Explain reasoning clearly

Return:
- risk_score between 0 and 1
- explanation
"""
