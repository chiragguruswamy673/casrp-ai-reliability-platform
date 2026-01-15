from collections import defaultdict

class VectorMemory:
    def __init__(self):
        self.entries = []
        self.failure_counts = defaultdict(int)

    def store(self, entry):
        self.entries.append(entry)

        # Track flaky tests
        snapshot = entry.get("snapshot", {})
        for failure in snapshot.get("recent_failures", []):
            test_name = failure.get("test_name")
            if test_name:
                self.failure_counts[test_name] += 1

    def retrieve_all(self):
        return self.entries

    def get_flaky_tests(self):
        result = []
        for test, count in self.failure_counts.items():
            if count >= 2:
                status = "highly_flaky" if count >= 3 else "flaky"
                result.append({
                    "test_name": test,
                    "failures": count,
                    "status": status
                })
        return result
