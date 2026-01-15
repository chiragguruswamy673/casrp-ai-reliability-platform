from fastapi import FastAPI
from datetime import datetime
import uuid
import xml.etree.ElementTree as ET
from fastapi import UploadFile, File
from digital_twin.state.system_state import SystemState
from digital_twin.event.event_schema import SystemEvent, EventType
from memory.vector_store import VectorMemory
from ai_agents.incident_summarizer import summarize_incident
from ai_agents.event_agent import EventAgent
from ai_agents.risk_agent import RiskAgent
from ai_agents.memory_agent import MemoryAgent
from ai_agents.orchestrator import Orchestrator
from ai_agents.healer_agent import HealerAgent
from ai_agents.flaky_analyzer import analyze_flaky_tests

app = FastAPI()

# --------------------------------------------------
# CORE SYSTEM COMPONENTS
# --------------------------------------------------
state = SystemState()
memory = VectorMemory()

# AI Agents
event_agent = EventAgent(state)
risk_agent = RiskAgent()
memory_agent = MemoryAgent(memory)
healer_agent = HealerAgent()

# Orchestrator (brain)
orchestrator = Orchestrator(
    state=state,
    memory=memory,
    event_agent=event_agent,
    risk_agent=risk_agent,
    memory_agent=memory_agent,
    healer_agent=healer_agent
)

# --------------------------------------------------
# 1️⃣ GET DIGITAL TWIN STATE + AI RISK
# --------------------------------------------------
@app.get("/twin/state")
def get_state():
    snapshot, risk = orchestrator.assess_risk()
    return {
        "state": snapshot,
        "risk_analysis": risk,
        "memory_entries": len(memory.retrieve_all())
    }

# --------------------------------------------------
# 2️⃣ INGEST CODE CHANGE EVENT
# --------------------------------------------------
@app.post("/event/code-change")
def code_change_event():
    event = SystemEvent(
        event_id=str(uuid.uuid4()),
        event_type=EventType.CODE_CHANGE,
        source="auth-service",
        payload={
            "files_changed": ["login.py", "auth_utils.py"]
        },
        timestamp=datetime.utcnow()
    )

    orchestrator.process_event(event)

    return {
        "message": "Code change event ingested",
        "event_id": event.event_id
    }

# --------------------------------------------------
# 3️⃣ INGEST DB MIGRATION EVENT
# --------------------------------------------------
@app.post("/event/db-migration")
def db_migration_event():
    event = SystemEvent(
        event_id=str(uuid.uuid4()),
        event_type=EventType.DB_MIGRATION,
        source="user-db",
        payload={
            "version": "v2_add_email_index"
        },
        timestamp=datetime.utcnow()
    )

    result = orchestrator.process_event(event)

    return {
        "message": "DB migration event ingested",
        "auto_assessed": result["auto_assessed"],
        "risk": result.get("risk")
    }

# --------------------------------------------------
# 4️⃣ INGEST TEST FAILURE EVENT
# --------------------------------------------------
@app.post("/event/test-failure")
def test_failure_event():
    event = SystemEvent(
        event_id=str(uuid.uuid4()),
        event_type=EventType.TEST_FAILURE,
        source="login-ui-tests",
        payload={
            "test_name": "test_invalid_login",
            "error": "ElementNotFoundException"
        },
        timestamp=datetime.utcnow()
    )

    result = orchestrator.process_event(event)

    return {
        "message": "Test failure event ingested",
        "auto_assessed": result["auto_assessed"],
        "risk": result.get("risk")
    }

# --------------------------------------------------
# 5️⃣ VIEW AI MEMORY (TEMPORAL INTELLIGENCE)
# --------------------------------------------------
@app.get("/twin/memory")
def view_memory():
    return {
        "memory": memory.retrieve_all()
    }

@app.get("/twin/heal")
def get_healing_suggestions():
    suggestions = orchestrator.suggest_healing()

    # Store what we suggested (learning)
    memory.store({
        "timestamp": datetime.utcnow().isoformat(),
        "healing_suggestions": [s.dict() for s in suggestions]
    })

    return {
        "risk_score": state.risk_score,
        "suggestions": suggestions
    }

@app.get("/twin/heal/actions")
def get_healing_actions():
    suggestions = orchestrator.suggest_healing()

    # Map suggestions to safe pipeline actions
    actions = []
    for s in suggestions:
        if "locator" in s.title.lower():
            actions.append({
                "action": "ui_stabilization",
                "scope": "ui-tests",
                "command": "echo 'Run UI locator stabilization checks'"
            })
        elif "migration" in s.title.lower():
            actions.append({
                "action": "db_validation",
                "scope": "database",
                "command": "echo 'Run DB smoke tests'"
            })
        elif "regression" in s.title.lower():
            actions.append({
                "action": "targeted_regression",
                "scope": "service",
                "command": "echo 'Run targeted regression suite'"
            })

    return {
        "risk_score": state.risk_score,
        "actions": actions
    }

@app.post("/ingest/testng")
async def ingest_testng_report(file: UploadFile = File(...)):
    content = await file.read()
    root = ET.fromstring(content)

    failures = []

    for test in root.iter("test-method"):
        status = test.attrib.get("status")
        if status == "FAIL":
            failures.append({
                "test_name": test.attrib.get("name"),
                "error": test.findtext("exception/message", default="Unknown error")
            })

    events_created = 0
    for failure in failures:
        event = SystemEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.TEST_FAILURE,
            source="testng-report",
            payload=failure,
            timestamp=datetime.utcnow()
        )
        orchestrator.process_event(event)
        events_created += 1

    return {
        "total_failures": len(failures),
        "events_created": events_created,
        "auto_assessed": True
    }

@app.get("/observe/incident")
def observe_incident():
    memory_entries = memory.retrieve_all()
    incident = summarize_incident(memory_entries)

    return {
        "incident": incident,
        "events_analyzed": len(memory_entries)
    }

@app.get("/observe/flaky")
def observe_flaky_tests():
    flaky_tests = memory.get_flaky_tests()
    analysis = analyze_flaky_tests(flaky_tests)

    return {
        "flaky_tests": flaky_tests,
        "analysis": analysis
    }

