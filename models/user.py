from dataclasses import dataclass


@dataclass
class UserState:
    user_id: str
    xp_total: int
    level: int
