import time
import random
import json
import os

file_path = "quiz_questions.json"
high_score_file = "high_score.json"

def clear_screen():
    print("\033[H\033[J", end="")

def choice(option_num: int) -> int:
    while True:
        try:
            value = int(input(f"Enter an option number between 1 and {option_num}: ").strip()) -1
            if 0 <= value < option_num:
                return value
            print(f"Please enter a number between 1 and {option_num}.")
        except ValueError:
            print("Invalid Input, Please enter a whole number.")

def read_questions_from_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
            if not isinstance(questions, list):
                print(f"Invalid format in {file_path}. Expected a list of questions.")
                return []
            return questions
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return []

def get_current_high_score():
    if not os.path.exists(high_score_file):
        return 0
    try:
        with open(high_score_file, "r", encoding = "utf-8") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    except Exception as e:
        print(f"Error reading high score: {e}")
        return 0
    
def check_and_save_high_score(score: int):
    previous_high_score = get_current_high_score()
    if score > previous_high_score:
        print(f"Congratulations! You've set a new high score: {score}")
        try:
            with open(high_score_file, "w", encoding="utf-8") as f:
                json.dump({"high_score": score}, f, indent=4)
        except Exception as e:
            print(f"Error saving high score: {e}")
    else:
        print(f"Your score: {score}. Current high score: {previous_high_score}")

def run_quiz(questions_data: list):
    score = 0

    random.shuffle(questions_data)
    for question_list in questions_data:
        random.shuffle(question_list["options"])

    try:
        for q_index, question_list in enumerate(questions_data, start = 1):
            clear_screen()

            print(f"{q_index}. {question_list['question']}")

            for opt_index, option in enumerate(question_list["options"], start = 1):
                print(f"{opt_index}. {option}")

            user_answer = choice(len(question_list["options"]))

            # Look up the actual string value the user selected
            selected_option_text = question_list["options"][user_answer]


            if selected_option_text == question_list["answer"]:
                score += 1
                print("Correct!")
            else:
                print(f"incorrect! The correct answer is: {question_list['answer']}")

            time.sleep(2)

        clear_screen()
        print("Quiz completed!")
        print(f"Your final score is: {score}/{len(questions_data)}")

        # Check if the final score is a new high score
        check_and_save_high_score(score)

    except KeyboardInterrupt:
        clear_screen()
        print(f"\nQuiz interrupted. Your final score is: {score}/{len(questions_data)}")

def main():
    while True:
        quiz_questions = read_questions_from_file(file_path)
        
        if not quiz_questions:
            print("Could not start quiz. Please ensure your JSON file exists and contains questions.")
            return
            
        run_quiz(quiz_questions)

        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        
        if play_again != 'y' and play_again != 'yes':
            clear_screen()
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()
