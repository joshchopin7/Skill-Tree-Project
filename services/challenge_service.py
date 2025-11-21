from typing import List, Tuple

from models.challenge import Challenge
from models.user import UserState
from repositories.challenge_repo import (
    get_all_challenges,
    mark_challenge_completed,
)
from repositories.user_repo import save_user
from services.xp_service import compute_level
from services.skill_tree_service import update_unlocks_for_user


def list_challenges() -> List[Challenge]:
    """Return all challenges with their completion status."""
    return get_all_challenges()


def complete_challenge(user: UserState, challenge_id: str) -> Tuple[bool, str, int]:
    """
    Try to complete a challenge for the user.

    Returns (success, message, xp_earned).
    - success: True if challenge newly completed, False otherwise
    - message: explanation for user
    - xp_earned: XP gained (0 if none)
    """
    challenges = get_all_challenges()
    challenge = next((c for c in challenges if c.challenge_id == challenge_id), None)

    if challenge is None:
        return False, "Challenge not found.", 0

    if challenge.is_completed:
        return False, "You already completed this challenge.", 0

    # Award XP
    user.xp_total += challenge.xp_reward
    user.level = compute_level(user.xp_total)
    save_user(user)

    # Unlock any skills that are now reachable by XP
    newly_unlocked = update_unlocks_for_user(user.xp_total)

    # Build user message
    base_msg = f"Challenge completed! You earned {challenge.xp_reward} XP."
    if newly_unlocked:
        unlocked_str = ", ".join(newly_unlocked)
        base_msg += f" New skills unlocked: {unlocked_str}."

    # Mark as completed in storage
    mark_challenge_completed(challenge_id)

    return True, base_msg, challenge.xp_reward
