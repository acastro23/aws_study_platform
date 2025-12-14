from aws_profile import ProfileStore
from quiz_core import load_questions
from aws_menu import main_menu


def main():
    """
    The basic rundown:
        A user enters their name, then it checks if its a returning user or new user. If it is a returning user, load their badges and output the main_menu() function call.
        If it is a new user, create a new profile and then load the main_menu() function call.
    """
    player_record = ProfileStore()

    name = input("Enter your trainer name: ").strip()
    if not name:
        name = "Guest"
    profile = player_record.get_or_create_player(name)

    if profile.badges:
        badge_list = ", ".join(sorted(profile.badges.keys()))
        print(f"\nWelcome back, {name}! You have these badges: {badge_list}\n")
    else:
        print(f"\nWelcome, {name}! New trainer profile created.\n")

    all_questions = load_questions()

    main_menu(profile, player_record, all_questions)


if __name__ == "__main__":
    main()