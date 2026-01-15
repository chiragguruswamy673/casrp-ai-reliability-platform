from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class EventType(str, Enum):
    CODE_CHANGE = "code_change"
    DB_MIGRATION = "db_migration"
    DEPLOYMENT = "deployment"
    TEST_FAILURE = "test_failure"
    PROD_ANOMALY = "prod_anomaly"

class SystemEvent(BaseModel):
    event_id: str
    event_type: EventType
    source: str
    payload: dict
    timestamp: datetime
