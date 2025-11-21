from typing import List

from models.skill_node import SkillNode
from repositories.skill_node_repo import (
    get_all_skill_nodes,
    mark_node_unlocked,
)


def list_skill_nodes() -> List[SkillNode]:
    """Return all skill nodes with their current unlocked/completed status."""
    return get_all_skill_nodes()


def update_unlocks_for_user(xp_total: int) -> list[str]:
    """
    Unlock any skill nodes whose xp_required is now met or exceeded.

    Returns a list of skill *names* that were newly unlocked.
    """
    nodes = get_all_skill_nodes()
    newly_unlocked: list[str] = []

    for node in nodes:
        if not node.is_unlocked and xp_total >= node.xp_required:
            # Mark as unlocked in persistent state
            mark_node_unlocked(node.node_id)
            newly_unlocked.append(node.name)

    return newly_unlocked
