from dataclasses import dataclass
from typing import Optional


@dataclass
class Challenge:
    challenge_id: str
    title: str
    xp_reward: int
    description: Optional[str] = None
    is_completed: bool = False
