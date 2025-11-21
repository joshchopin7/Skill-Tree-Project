from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillNode:
    node_id: str
    name: str
    xp_required: int
    order: int
    description: Optional[str] = None
    is_unlocked: bool = False
    is_completed: bool = False
