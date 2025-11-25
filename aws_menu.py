from quiz_core import choose_badge, run_quiz_for_badge, passing_score


def show_profile(profile):
    print("\n====== Player Profile ======")
    print(f"Name: {profile.name}")
    print(f"Total quizzes taken: {profile.total_quizzes}")
    print(f"Total correct answers: {profile.total_correct}")

    if profile.total_quizzes > 0:
        accuracy = (profile.total_correct / (profile.total_quizzes * 1.0)) * 100
        print(f"Overall accuracy: {accuracy:.2f} percent")
    else:
        print("Overall accuracy: N/A")
    print("============================\n")


def show_badges(profile):
    print("\n====== Earned Badges ======")
    if not profile.badges:
        print("You have not earned any badges yet.")
    else:
        for badge, info in profile.badges.items():
            print(f"{badge} Badge - Best Score: {info['best_score']} percent")
    print("===========================\n")    


def main_menu(profile, store, all_questions):
    while True:
        print("====== AWS Practice Game Menu ======")
        print("1. Start a quiz")
        print("2. View profile stats")
        print("3. View earned badges")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            badge_name = choose_badge(all_questions)
            score, total = run_quiz_for_badge(badge_name, all_questions, num_questions=5)

            if total == 0:
                print("Returning to menu...")
                continue

            percent, previous_best = profile.record_quiz_result(
                badge_name = badge_name,
                score = score,
                total = total,
                pass_percentage = passing_score,
            )
            print(f"\nYou scored {percent:.2f}% on the {badge_name} quiz.")
        
            if percent >= passing_score:
                if previous_best < passing_score:
                    # This is a reminder comment of this logic --> this if condition works as it assumes you have not earned a badge yet, hence previous_best would be 0
                    print(f"Good job, {profile.name}! You just earned the {badge_name} badge!\n")
                else:
                    print(f"You kept your {badge_name} badge abd improved your score!")
            else:
                if previous_best >= passing_score:
                    print(f"You already earned this badge before, and your best score was: {previous_best:.2f}.")
                else:
                    print("You have not earned this badge. ?Keep trying!")
            store.update_profile(profile)
        
        elif choice == "2":
            show_profile(profile)
        
        elif choice == "3":
            show_badges(profile)
        
        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Please enter a valid choice...\n")