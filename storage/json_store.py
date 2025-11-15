import json
from pathlib import Path


STORAGE_DIR = Path(__file__).resolve().parent  # points to /storage


def load_json(filename: str, default_data):
    """Load JSON from storage/<filename>, or return default_data if missing."""
    file_path = STORAGE_DIR / filename

    if not file_path.exists():
        return default_data

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename: str, data):
    """Save JSON to storage/<filename> (overwrite)."""
    file_path = STORAGE_DIR / filename
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
