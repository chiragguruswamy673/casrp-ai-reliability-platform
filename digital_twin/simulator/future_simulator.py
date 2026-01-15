def simulate_future(state_snapshot, hypothetical_event):
    simulated = state_snapshot.copy()

    if hypothetical_event["type"] == "traffic_spike":
        simulated["risk_score"] += 0.2

    if hypothetical_event["type"] == "schema_change":
        simulated["risk_score"] += 0.3

    return simulated
