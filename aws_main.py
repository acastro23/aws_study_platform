import json, random
from aws_profile import ProfileStore, PlayerProfile, profile_path


questions_path = "aws_questions.json"
passing_score = 80

def load_questions(path=questions_path):
    """ All questions are pulled from the 'aws_questions.json' file. """
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ask_question(q):
    print("\nQuestion:", q["question"], "\n")

    options = q["options"][:]
    correct_option = options[q["answer_index"]]

    random.shuffle(options)

    for idx, option_text in enumerate(options, start=1):
        print(f"{idx}. {option_text}")

    while True:
        try:
            choice = int(input("\nEnter your answer: "))
            if 1 <= choice <= len(options):
                break
            else:
                print("Enter a valid number.")
        except ValueError:
            print("Enter a number, not text.")

    chosen_option = options[choice - 1]
    is_correct = (chosen_option == correct_option)

    if is_correct:
        print("Correct!")
    else:
        print(f"Incorrect. The correct answer was: {correct_option}")

    print("Explanation:", q["explanation"])
    return is_correct


def choose_badge(all_questions):
    """The player should be able to choose the aws domain, in this program they are known as badges"""

    domains = sorted({q["category"] for q in all_questions})
    print("These are the available topics: ")
    for idx, cat in enumerate(domains, start=1):
        print(f"{idx}. {cat}")
    

    while True:
        try:
            choice = int(input("\nPick a badge by number: "))
            if 1 <= choice <= len(domains):
                return domains[choice - 1]
            else:
                print("Please enter a valid choice from the list!")
        except ValueError:
            print("Please enter a number, not text")



def run_quiz_for_badge(badge_name, all_questions, num_questions=5):
    """
    Here, we will run a quiz for a particular badge and return the score along with the total questions for that domain
    """

    badge_questions = [q for q in all_questions if q["category"] == badge_name]
    if not badge_questions:
        print(f"No questions found for badge: {badge_name}")
        return 0, 0
    
    random.shuffle(badge_questions)
    badge_questions = badge_questions[:num_questions]
    total = len(badge_questions)

    print("\nWelcome to AWS study app")
    print(f"You will face {total} questions on {badge_name} to earn your badge.\n")

    score = 0
    for q in badge_questions:
        if ask_question(q):
            score += 1
    print("\nYou have completed the quiz!")
    print(f"Your final score was {score} / {total}")
    return score, total


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
    badge_name = choose_badge(all_questions)

    score, total = run_quiz_for_badge(badge_name, all_questions, num_questions=5)
    if total == 0:
        print("No questions for this badge. Exiting.")
        return

    percent, previous_best = profile.record_quiz_result(
        badge_name=badge_name,
        score=score,
        total=total,
        pass_percentage=passing_score,
    )

    print(f"You scored {percent:.2f} percent on the {badge_name} quiz.")

    if percent >= passing_score:
        if previous_best < passing_score:
            print(f"\nNice job, {name}! You earned the {badge_name} Badge!")
        else:
            print(f"\nYou kept your {badge_name} Badge and improved your best score.")
    else:
        if previous_best >= passing_score:
            print(
                f"\nYou already earned the {badge_name} Badge before. "
                f"Your best score is still {previous_best:.2f} percent. Keep practicing."
            )
        else:
            print(
                f"\nYou did not reach {passing_score} percent yet. "
                "Keep training and try again for this badge."
            )

    store.update_profile(profile)
    print(f"\nProfile saved to {profile_path}. Thanks for playing.\n")



if __name__ == "__main__":
    main()