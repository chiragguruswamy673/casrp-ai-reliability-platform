from ai_agents.risk_predictor import predict_risk

class RiskAgent:
    def evaluate(self, snapshot: dict) -> dict:
        return predict_risk(snapshot)
