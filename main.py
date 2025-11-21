from repositories.user_repo import load_user, save_user
from repositories.session_repo import load_sessions
from services.session_service import log_session_for_user
from services.challenge_service import list_challenges, complete_challenge
from services.skill_tree_service import list_skill_nodes, update_unlocks_for_user


def main_menu():
    # Load existing user or create a default one
    user = load_user()

    while True:
        print("\n🌊 Surf Skill Tree CLI 🌊")
        print(f"User: {user.user_id} | XP: {user.xp_total} | Level: {user.level}")
        print("----------------------------------------")
        print("1) Log a Surf Session")
        print("2) View Progress")
        print("3) View Session History")
        print("4) View / Complete Challenges")
        print("5) View Skill Tree")
        print("6) Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            handle_log_session(user)
        elif choice == "2":
            handle_view_progress(user)
        elif choice == "3":
            handle_view_history()
        elif choice == "4":
            handle_challenges(user)
        elif choice == "5":
            handle_view_skill_tree()
        elif choice == "6":
            print("Saving progress... 💾")
            save_user(user)
            print("Goodbye, surfer! 🤙")
            break
        else:
            print("\nInvalid choice — please try again.\n")


def handle_log_session(user):
    print("\n📝 Log a Surf Session")

    session_date = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    spot = input("Surf spot (optional): ").strip()

    # Get a valid duration
    while True:
        duration_str = input("Duration in minutes: ").strip()
        try:
            duration_min = int(duration_str)
            if duration_min <= 0:
                print("Please enter a positive number of minutes.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for minutes.")

    notes = input("Notes (optional): ").strip()

    session = log_session_for_user(
        user=user,
        session_date=session_date,
        spot=spot,
        duration_min=duration_min,
        notes=notes,
    )

    # After XP update, see if any new skills unlocked
    newly_unlocked = update_unlocks_for_user(user.xp_total)

    print(f"\n✅ Session logged! You earned {session.xp_earned} XP.")
    print(f"New total XP: {user.xp_total} | Level: {user.level}")

    if newly_unlocked:
        print("🎉 New skills unlocked:")
        for name in newly_unlocked:
            print(f"  • {name}")
    print()


def handle_view_progress(user):
    print("\n📊 Current Progress")
    print(f"Total XP: {user.xp_total}")
    print(f"Level:    {user.level}")
    print()


def handle_view_history():
    print("\n📘 Surf Session History\n")

    sessions = load_sessions()

    if not sessions:
        print("No sessions logged yet.\n")
        return

    for i, s in enumerate(sessions, start=1):
        print(f"Session {i}")
        print(f"  Date:      {s.date_iso}")
        print(f"  Spot:      {s.spot or '—'}")
        print(f"  Duration:  {s.duration_min} minutes")
        print(f"  XP Earned: {s.xp_earned}")
        print(f"  Notes:     {s.notes or '—'}")
        print("-----------------------------------")

    print()  # extra newline at end


def handle_challenges(user):
    print("\n🏆 Challenges\n")

    challenges = list_challenges()

    if not challenges:
        print("No challenges defined yet.\n")
        return

    for idx, ch in enumerate(challenges, start=1):
        status = "✅ DONE" if ch.is_completed else "⬜ TODO"
        print(f"{idx}) {ch.title} [{status}]")
        print(f"   XP Reward: {ch.xp_reward}")
        if ch.description:
            print(f"   {ch.description}")
        print()

    choice = input("Enter challenge number to complete (or press Enter to go back): ").strip()
    if not choice:
        return

    try:
        index = int(choice)
    except ValueError:
        print("Invalid input. Returning to main menu.\n")
        return

    if index < 1 or index > len(challenges):
        print("Invalid challenge number. Returning to main menu.\n")
        return

    selected = challenges[index - 1]
    success, message, xp_earned = complete_challenge(user, selected.challenge_id)

    print()
    print(message)
    if success:
        print(f"New total XP: {user.xp_total} | Level: {user.level}")
    print()


def handle_view_skill_tree():
    print("\n🌱 Skill Tree — Foamie Path\n")

    nodes = list_skill_nodes()

    if not nodes:
        print("No skill nodes defined yet.\n")
        return

    for node in nodes:
        if node.is_completed:
            status = "✅ COMPLETED"
        elif node.is_unlocked:
            status = "🔓 UNLOCKED"
        else:
            status = "🔒 LOCKED"

        print(f"{node.order}. {node.name} [{status}]")
        print(f"   XP Required: {node.xp_required}")
        if node.description:
            print(f"   {node.description}")
        print()

    print()

if __name__ == "__main__":
    main_menu()
