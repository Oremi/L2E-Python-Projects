import time
import random
import json

file_path = "quiz_questions.json"

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
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
            return questions
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return []

def run_quiz(questions_data: list):
    score = 0

    random.shuffle(questions_data)
    for question_list in questions_data:
        random.shuffle(question_list["options"])

    try:
        for q_index, question_list in enumerate(questions_data, start = 1):
            clear_screen()

            print(f"{q_index}. {question_list['question']}")

            for q_index, option in enumerate(question_list["options"], start = 1):
                print(f"{q_index}. {option}")

            user_answer = choice(len(question_list["options"]))

            # Look up the actual string value the user selected
            selected_option_text = question_list["options"][user_answer]


            if selected_option_text == question_list["answer"]:
                score += 1
                print("Correct!")
            else:
                correct_option = question_list["options"][question_list["answer"]]
                print(f"incorrect! The correct answer is: {correct_option}")

            time.sleep(2)

        clear_screen()
        print("Quiz completed!")
        print(f"Your final score is: {score}/{len(questions_data)}")

    except KeyboardInterrupt:
        clear_screen()
        print(f"\nQuiz interrupted. Your final score is: {score}/{len(questions_data)}")

def main():
    quiz_questions = read_questions_from_file(file_path)
    
    if not quiz_questions:
        print("Could not start quiz. Please ensure your JSON file exists and contains questions.")
        return
        
    run_quiz(quiz_questions)

if __name__ == "__main__":
    main()
