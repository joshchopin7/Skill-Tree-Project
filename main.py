from repositories.user_repo import load_user, save_user
from repositories.session_repo import load_sessions
from services.session_service import log_session_for_user


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
        print("4) Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            handle_log_session(user)
        elif choice == "2":
            handle_view_progress(user)
        elif choice == "3":
            handle_view_history()
        elif choice == "4":
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

    print(f"\n✅ Session logged! You earned {session.xp_earned} XP.")
    print(f"New total XP: {user.xp_total} | Level: {user.level}\n")


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


if __name__ == "__main__":
    main_menu()
