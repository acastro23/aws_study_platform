import json
import random


def load_questions(path="aws_questions.json"):
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


def run_quiz(num_questions=5):
    questions = load_questions()
    random.shuffle(questions)
    questions = questions[:num_questions]

    print("Welcome to AWS training")
    print(f"You will have to face through {num_questions} to earn your badge!\n")

    score=0
    for q in questions:
        if ask_question(q):
            score+=1
    print("\nQuiz Complete")
    print(f"Your final score was: {score} / {num_questions}")





if __name__ == "__main__":
    run_quiz()