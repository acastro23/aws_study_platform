from aws_profile import ProfileStore
from quiz_core import load_questions
from aws_menu import main_menu


def main():
    store = ProfileStore()

    name = input("Enter your trainer name: ").strip()
    if not name:
        name = "Guest"

    profile = store.get_or_create_player(name)

    if profile.badges:
        badge_list = ", ".join(sorted(profile.badges.keys()))
        print(f"\nWelcome back, {name}! You have these badges: {badge_list}\n")
    else:
        print(f"\nWelcome, {name}! New trainer profile created.\n")

    all_questions = load_questions()

    main_menu(profile, store, all_questions)


if __name__ == "__main__":
    main()