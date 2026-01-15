from ai_agents.remediation import Remediation

class HealerAgent:
    def suggest(self, snapshot: dict, risk: dict):
        suggestions = []

        # TEST FAILURE HEALING
        if snapshot.get("recent_failures"):
            suggestions.append(Remediation(
                title="Stabilize flaky UI locator",
                description=(
                    "Recent UI test failure indicates a brittle locator. "
                    "Recommend switching to data-testid or improving waits."
                ),
                confidence=0.78,
                blast_radius="low",
                command_hint="Update locator strategy; add explicit waits."
            ))

        # DB MIGRATION HEALING
        if snapshot.get("db_schema_version"):
            suggestions.append(Remediation(
                title="Validate DB migration",
                description=(
                    "Database schema changed. Recommend running migration checks "
                    "and rolling forward only after smoke tests pass."
                ),
                confidence=0.85,
                blast_radius="medium",
                command_hint="Run DB smoke tests; verify backward compatibility."
            ))

        # CODE CHANGE HEALING
        if snapshot.get("services"):
            suggestions.append(Remediation(
                title="Targeted regression testing",
                description=(
                    "Service code changed. Recommend running targeted regression "
                    "tests for affected endpoints."
                ),
                confidence=0.65,
                blast_radius="low",
                command_hint="Run service-scoped regression suite."
            ))

        return suggestions
