from uuid import uuid4
from datetime import date

from models.user import UserState
from models.session import Session
from repositories.session_repo import add_session
from repositories.user_repo import save_user
from services.xp_service import compute_session_xp, compute_level


def log_session_for_user(
    user: UserState,
    session_date: str,
    spot: str | None,
    duration_min: int,
    notes: str | None,
) -> Session:
    """
    Create a session, compute XP, update user XP/level, and persist.
    Returns the Session object.
    """
    # If user just hits enter for date, default to today
    if not session_date.strip():
        session_date = date.today().isoformat()

    xp = compute_session_xp(duration_min)

    # Update user
    user.xp_total += xp
    user.level = compute_level(user.xp_total)
    save_user(user)

    # Create session
    session = Session(
        session_id=str(uuid4()),
        date_iso=session_date,
        spot=spot or None,
        duration_min=duration_min,
        notes=notes or None,
        xp_earned=xp,
    )

    # Persist session
    add_session(session)

    return session
