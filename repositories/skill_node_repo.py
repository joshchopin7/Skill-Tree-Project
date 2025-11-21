from pathlib import Path
from typing import List, Tuple

from models.skill_node import SkillNode
from storage.json_store import load_json, save_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SKILL_TREE_FILE = DATA_DIR / "skill_tree.json"
SKILL_STATE_FILE = "skill_tree_state.json"   # in storage/


def _load_skill_definitions() -> List[SkillNode]:
    """Load static skill node definitions from data/skill_tree.json."""
    if not SKILL_TREE_FILE.exists():
        return []

    import json
    with SKILL_TREE_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    nodes: List[SkillNode] = []
    for item in raw.get("nodes", []):
        nodes.append(
            SkillNode(
                node_id=item["id"],
                name=item["name"],
                xp_required=int(item["xp_required"]),
                order=int(item["order"]),
                description=item.get("description"),
                is_unlocked=False,
                is_completed=False,
            )
        )
    # sort by order just in case
    nodes.sort(key=lambda n: n.order)
    return nodes


def _load_state() -> Tuple[set[str], set[str]]:
    """
    Load unlocked and completed node ids.
    By default, first node (n1) is unlocked.
    """
    default = {"unlocked_ids": ["n1"], "completed_ids": []}
    data = load_json(SKILL_STATE_FILE, default)
    unlocked_ids = set(data.get("unlocked_ids", []))
    completed_ids = set(data.get("completed_ids", []))
    return unlocked_ids, completed_ids


def _save_state(unlocked_ids: set[str], completed_ids: set[str]) -> None:
    data = {
        "unlocked_ids": list(unlocked_ids),
        "completed_ids": list(completed_ids),
    }
    save_json(SKILL_STATE_FILE, data)


def get_all_skill_nodes() -> List[SkillNode]:
    """Return all skill nodes with their current unlocked/completed status."""
    nodes = _load_skill_definitions()
    unlocked_ids, completed_ids = _load_state()

    for node in nodes:
        if node.node_id in unlocked_ids:
            node.is_unlocked = True
        if node.node_id in completed_ids:
            node.is_completed = True

    return nodes


def mark_node_unlocked(node_id: str) -> None:
    unlocked_ids, completed_ids = _load_state()
    unlocked_ids.add(node_id)
    _save_state(unlocked_ids, completed_ids)


def mark_node_completed(node_id: str) -> None:
    unlocked_ids, completed_ids = _load_state()
    completed_ids.add(node_id)
    _save_state(unlocked_ids, completed_ids)
