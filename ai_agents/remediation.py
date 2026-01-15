from pydantic import BaseModel
from typing import Optional

class Remediation(BaseModel):
    title: str
    description: str
    confidence: float  # 0..1
    blast_radius: str  # low | medium | high
    requires_approval: bool = True
    command_hint: Optional[str] = None
