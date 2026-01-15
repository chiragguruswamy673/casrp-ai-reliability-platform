import copy
from datetime import datetime

class MemoryAgent:
    def __init__(self, memory_store):
        self.memory = memory_store

    def remember(self, snapshot: dict, risk: dict):
        self.memory.store({
            "timestamp": datetime.utcnow().isoformat(),
            "snapshot": copy.deepcopy(snapshot),
            "risk": copy.deepcopy(risk)
        })
