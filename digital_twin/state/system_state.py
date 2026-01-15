class SystemState:
    def __init__(self):
        self.services = {}
        self.db_schema_version = None
        self.recent_failures = []
        self.risk_score = 0.0

    def update(self, event):
        if event.event_type == "code_change":
            self.services[event.source] = "modified"

        elif event.event_type == "db_migration":
            self.db_schema_version = event.payload.get("version")

        elif event.event_type == "test_failure":
            self.recent_failures.append(event.payload)

    def snapshot(self):
        return {
            "services": self.services,
            "db_schema_version": self.db_schema_version,
            "recent_failures": self.recent_failures,
            "risk_score": self.risk_score
        }
