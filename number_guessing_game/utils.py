import json
import os

HIGH_SCORE_FILE = "high_scores.json"


def get_valid_int(prompt: str, min_val: int = 1, max_val: int = 100) -> int:
    while True:
        try:
            user_input = input(prompt).strip()
            num = int(user_input)
            if min_val <= num <= max_val:
                return num
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def calculate_score(attempts: int, max_attempts: int, max_range: int) -> int:
    """
    Calculate score based on:
        - attempts used (fewer = better)
        - difficulty (range size and max attempts)
    Formula: base = (max_range // 2) * (max_attempts - attempts + 1)
    """
    if attempts == 0 or attempts > max_attempts:
        return 0
    base = (max_range // 2) * (max_attempts - attempts + 1)
    return max(100, base)  # minimum 100 points


def load_high_scores() -> dict:
    if not os.path.exists(HIGH_SCORE_FILE):
        return {"easy": None, "medium": None, "hard": None}
    with open(HIGH_SCORE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"easy": None, "medium": None, "hard": None}


def save_high_score(difficulty: str, score: int, attempts: int):
    scores = load_high_scores()
    if scores.get(difficulty) is None or score > scores[difficulty]["score"]:
        scores[difficulty] = {"score": score, "attempts": attempts}
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=2)
        print(f"🎉 New high score for {difficulty} difficulty!")