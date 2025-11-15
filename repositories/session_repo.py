from typing import List
from uuid import uuid4

from models.session import Session
from storage.json_store import load_json, save_json


SESSIONS_FILE = "sessions.json"


def load_sessions() -> List[Session]:
    raw = load_json(SESSIONS_FILE, {"sessions": []})
    sessions = []
    for item in raw.get("sessions", []):
        sessions.append(
            Session(
                session_id=item.get("session_id", str(uuid4())),
                date_iso=item["date_iso"],
                spot=item.get("spot"),
                duration_min=int(item["duration_min"]),
                notes=item.get("notes"),
                xp_earned=int(item["xp_earned"]),
                applied_node_id=item.get("applied_node_id"),
            )
        )
    return sessions


def save_sessions(sessions: List[Session]) -> None:
    data = {
        "sessions": [
            {
                "session_id": s.session_id,
                "date_iso": s.date_iso,
                "spot": s.spot,
                "duration_min": s.duration_min,
                "notes": s.notes,
                "xp_earned": s.xp_earned,
                "applied_node_id": s.applied_node_id,
            }
            for s in sessions
        ]
    }
    save_json(SESSIONS_FILE, data)


def add_session(session: Session) -> None:
    sessions = load_sessions()
    sessions.append(session)
    save_sessions(sessions)
