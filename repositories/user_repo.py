from pathlib import Path

from models.user import UserState
from storage.json_store import load_json, save_json


USER_FILE = "user_data.json"


def load_user() -> UserState:
    """Load user data from JSON, or create a default user if none exists."""
    default_data = {
        "user_id": "default",
        "xp_total": 0,
        "level": 0,
    }

    data = load_json(USER_FILE, default_data)

    # Ensure all keys present, in case file is older / partially written
    user_id = data.get("user_id", "default")
    xp_total = int(data.get("xp_total", 0))
    level = int(data.get("level", 0))

    return UserState(user_id=user_id, xp_total=xp_total, level=level)


def save_user(user: UserState) -> None:
    """Persist user data to JSON."""
    data = {
        "user_id": user.user_id,
        "xp_total": user.xp_total,
        "level": user.level,
    }
    save_json(USER_FILE, data)
