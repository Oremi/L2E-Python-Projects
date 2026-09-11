from utils import get_valid_int, calculate_score, load_high_scores, save_high_score
import random

DIFFICULTIES = {
    "easy":   {"range": (1, 50),   "attempts": 10},
    "medium": {"range": (1, 100),  "attempts": 7},
    "hard":   {"range": (1, 200),  "attempts": 5},
}


def choose_difficulty() -> tuple:
    print("\nSelect difficulty:")
    print("[1] Easy   (1-50, 10 tries)")
    print("[2] Medium (1-100, 7 tries)")
    print("[3] Hard   (1-200, 5 tries)")
    
    while True:
        choice = get_valid_int("> ", 1, 3)
        if choice == 1:
            diff = "easy"
        elif choice == 2:
            diff = "medium"
        else:
            diff = "hard"
        r_min, r_max = DIFFICULTIES[diff]["range"]
        max_attempts = DIFFICULTIES[diff]["attempts"]
        return diff, r_min, r_max, max_attempts


def play_game():
    # Show high scores
    scores = load_high_scores()
    print("\n--- Current High Scores ---")
    for diff in ["easy", "medium", "hard"]:
        entry = scores.get(diff)
        if entry:
            print(f"{diff.capitalize()}: {entry['score']} pts ({entry['attempts']} attempts)")
        else:
            print(f"{diff.capitalize()}: None")
    print("----------------------------")

    # Choose difficulty
    difficulty, low, high, max_attempts = choose_difficulty()
    secret = random.randint(low, high)
    attempts_used = 0
    won = False

    print(f"\nI'm thinking of a number between {low} and {high}.")
    print(f"You have {max_attempts} attempts.\n")

    # Game loop
    while attempts_used < max_attempts and not won:
        remaining = max_attempts - attempts_used
        prompt = f"Attempt {attempts_used+1}/{max_attempts} — Enter your guess: "
        guess = get_valid_int(prompt, low, high)
        attempts_used += 1

        if guess < secret:
            print("📉 Too low! Try higher.")
        elif guess > secret:
            print("📈 Too high! Try lower.")
        else:
            won = True
            print(f"🎉 Correct! You got it in {attempts_used} attempt{'s' if attempts_used > 1 else ''}!")

    # End of round
    if won:
        score = calculate_score(attempts_used, max_attempts, high - low + 1)
        print(f"Your score: {score} points")
        # Update high score
        save_high_score(difficulty, score, attempts_used)
    else:
        print(f"😞 Out of attempts! The number was {secret}.")
        print("Better luck next time.")

    # Show updated high scores
    print("\n--- Updated High Scores ---")
    scores = load_high_scores()
    for diff in ["easy", "medium", "hard"]:
        entry = scores.get(diff)
        if entry:
            print(f"{diff.capitalize()}: {entry['score']} pts ({entry['attempts']} attempts)")
        else:
            print(f"{diff.capitalize()}: None")
    print("----------------------------")


def main():
    print("Welcome to the Number Guessing Game!")
    while True:
        play_game()

        while True:
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again in ('y', 'n'):
                break
            print("Please answer 'y' or 'n'.")
        if again == 'n':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()