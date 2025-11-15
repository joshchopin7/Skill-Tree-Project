def compute_session_xp(duration_min: int) -> int:
    """
    Base rule:
    - 5 XP per session
    - +1 XP per 10 minutes of surfing
    - Bonus capped so total <= 15 XP
    """
    base_xp = 5
    bonus = duration_min // 10   # 1 XP per 10 minutes
    xp = base_xp + bonus
    return min(xp, 15)           # cap at 15 XP


def compute_level(xp_total: int) -> int:
    """
    Simple level formula: 100 XP per level.
    """
    return xp_total // 100
