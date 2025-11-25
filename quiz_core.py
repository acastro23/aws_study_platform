# quiz_core.py
import json
import random

questions_path = "aws_questions.json"
passing_score = 80


def load_questions(path=questions_path):
    """All questions are pulled from the 'aws_questions.json' file."""
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
    """The player should be able to choose the aws domain, known here as badges."""
    domains = sorted({q["category"] for q in all_questions})
    print("These are the available topics:")
    for idx, cat in enumerate(domains, start=1):
        print(f"{idx}. {cat}")

    while True:
        try:
            choice = int(input("\nPick a badge by number: "))
            if 1 <= choice <= len(domains):
                return domains[choice - 1]
            else:
                print("Please enter a valid choice from the list.")
        except ValueError:
            print("Please enter a number, not text.")


def run_quiz_for_badge(badge_name, all_questions, num_questions=5):
    """Run a quiz for a particular badge and return (score, total_questions)."""
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
