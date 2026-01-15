from digital_twin.event.event_schema import EventType

class Orchestrator:
    def __init__(self, state, memory, event_agent, risk_agent, memory_agent, healer_agent=None):
        self.state = state
        self.event_agent = event_agent
        self.risk_agent = risk_agent
        self.memory_agent = memory_agent
        self.healer_agent = healer_agent

    def is_critical_event(self, event_type: EventType) -> bool:
        return event_type in [
            EventType.DB_MIGRATION,
            EventType.TEST_FAILURE
        ]

    def process_event(self, event):
        # Update state
        self.event_agent.handle(event)

        # AUTO intelligence for critical events
        if self.is_critical_event(event.event_type):
            snapshot = self.state.snapshot()
            risk = self.risk_agent.evaluate(snapshot)
            self.state.risk_score = risk["risk_score"]
            self.memory_agent.remember(snapshot, risk)

            return {
                "status": "state_updated",
                "auto_assessed": True,
                "risk": risk
            }

        return {
            "status": "state_updated",
            "auto_assessed": False
        }

    def assess_risk(self):
        snapshot = self.state.snapshot()
        risk = self.risk_agent.evaluate(snapshot)
        self.state.risk_score = risk["risk_score"]
        self.memory_agent.remember(snapshot, risk)
        return snapshot, risk
    
    def suggest_healing(self):
        snapshot = self.state.snapshot()
        risk = {
            "risk_score": self.state.risk_score
        }
        if not self.healer_agent:
            return []
        return self.healer_agent.suggest(snapshot, risk)
