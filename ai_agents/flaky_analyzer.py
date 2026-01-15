def analyze_flaky_tests(flaky_tests):
    if not flaky_tests:
        return {
            "flaky_detected": False,
            "summary": "No flaky tests detected."
        }

    worst = max(flaky_tests, key=lambda x: x["failures"])

    return {
        "flaky_detected": True,
        "worst_test": worst["test_name"],
        "failures": worst["failures"],
        "status": worst["status"],
        "recommendation": (
            "Test is flaky. Recommend stabilizing selectors, waits, "
            "and isolating external dependencies."
        )
    }
