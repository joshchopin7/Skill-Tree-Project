from dataclasses import dataclass
from typing import Optional


@dataclass
class Session:
    session_id: str
    date_iso: str
    spot: Optional[str]
    duration_min: int
    notes: Optional[str]
    xp_earned: int
    applied_node_id: Optional[str] = None
