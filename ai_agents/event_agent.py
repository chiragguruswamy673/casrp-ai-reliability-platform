class EventAgent:
    def __init__(self, system_state):
        self.state = system_state

    def handle(self, event):
        self.state.update(event)
        return {
            "status": "state_updated",
            "event_type": event.event_type
        }