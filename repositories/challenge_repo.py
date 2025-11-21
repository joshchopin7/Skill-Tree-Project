from pathlib import Path
from typing import List

from models.challenge import Challenge
from storage.json_store import load_json, save_json

# Paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CHALLENGES_FILE = DATA_DIR / "challenges.json"
CHALLENGES_STATE_FILE = "challenges_state.json"  # in storage/


def _load_challenge_definitions() -> List[Challenge]:
    """Load static challenge definitions from data/challenges.json."""
    if not CHALLENGES_FILE.exists():
        return []

    import json
    with CHALLENGES_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    challenges: List[Challenge] = []
    for item in raw.get("challenges", []):
        challenges.append(
            Challenge(
                challenge_id=item["id"],
                title=item["title"],
                xp_reward=int(item["xp"]),
                description=item.get("description"),
                is_completed=False,  # completion handled separately
            )
        )
    return challenges


def _load_completed_ids() -> set[str]:
    """Load which challenges have been completed by the user."""
    data = load_json(CHALLENGES_STATE_FILE, {"completed_ids": []})
    return set(data.get("completed_ids", []))


def _save_completed_ids(completed_ids: set[str]) -> None:
    data = {"completed_ids": list(completed_ids)}
    save_json(CHALLENGES_STATE_FILE, data)


def get_all_challenges() -> List[Challenge]:
    """Return all challenges with their current completion status."""
    base = _load_challenge_definitions()
    completed_ids = _load_completed_ids()

    for ch in base:
        if ch.challenge_id in completed_ids:
            ch.is_completed = True
    return base


def mark_challenge_completed(challenge_id: str) -> None:
    """Mark a challenge as completed (idempotent)."""
    completed_ids = _load_completed_ids()
    completed_ids.add(challenge_id)
    _save_completed_ids(completed_ids)
