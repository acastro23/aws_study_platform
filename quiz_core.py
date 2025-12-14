import json, random
from config import QUESTIONS_PATH


def load_questions(path=QUESTIONS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ask_question(q):
    print("\nQuestion:", q["question"], "\n")

    options = q["options"][:]
    correct_option = options[q["answer_index"]]

    random.shuffle(options)

    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    while True:
        try:
            choice = int(input("\nEnter your answer: "))
            if 1 <= choice <= len(options):
                break
            print("Enter a valid number.")
        except ValueError:
            print("Enter a number, not text.")

    chosen_option = options[choice - 1]
    is_correct = chosen_option == correct_option

    if is_correct:
        print("Correct!")
    else:
        print(f"Incorrect. Correct answer: {correct_option}")

    print("Explanation:", q["explanation"])

    return is_correct, chosen_option, correct_option


def choose_badge(all_questions):
    domains = sorted({q["category"] for q in all_questions})

    print("\nAvailable topics:")
    for i, d in enumerate(domains, start=1):
        print(f"{i}. {d}")

    while True:
        try:
            choice = int(input("\nPick a badge: "))
            if 1 <= choice <= len(domains):
                return domains[choice - 1]
            print("Invalid choice.")
        except ValueError:
            print("Enter a number.")


def review_missed_questions(missed):
    print("\n====== Review Missed Questions ======")

    for i, m in enumerate(missed, start=1):
        print(f"\n[{i}] Topic: {m['category']}")
        print("Question:", m["question"])
        print("Your answer:", m["your_answer"])
        print("Correct answer:", m["correct_answer"])
        print("Explanation:", m["explanation"])
        input("\nPress Enter to continue...")
        print()
    
    while True:
        done = input("Are you done reviewing? (y/n): ").strip().lower()
        if done in ('y', 'n'):
            break
        print("Please enter y for yes or n for no.")
    
    if done == "n":
        review_missed_questions(missed)
    print("Returning you back to main meun...\n")



def run_quiz_for_badge(badge_name, all_questions, num_questions):
    badge_questions = [q for q in all_questions if q["category"] == badge_name]

    if not badge_questions:
        print("No questions found.")
        return 0, 0

    random.shuffle(badge_questions)
    quiz_questions = badge_questions[:num_questions]

    score = 0
    missed = []

    print(f"\nStarting {badge_name} quiz ({len(quiz_questions)} questions)\n")

    for q in quiz_questions:
        is_correct, chosen, correct = ask_question(q)
        if is_correct:
            score += 1
        else:
            missed.append({
                "category": q["category"],
                "question": q["question"],
                "your_answer": chosen,
                "correct_answer": correct,
                "explanation": q["explanation"],
            })

    print(f"\nFinal Score: {score} / {len(quiz_questions)}")

    if missed:
        review = input("\nReview missed questions now? (y/n): ").strip().lower()
        if review == "y":
            review_missed_questions(missed)

    return score, len(quiz_questions)