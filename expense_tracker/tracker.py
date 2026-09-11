import datetime
import json
import os

expenses = []
last_saved = []

APP_DIR = os.path.join(os.path.expanduser("~"), ".expense_tracker")
os.makedirs(APP_DIR, exist_ok=True)
DATA_FILE = os.path.join(APP_DIR, "expenses.json")

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_valid_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid Input, Please enter a whole number.")

def get_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty. Please try again.")
            continue
        return value

def get_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_expense():
    amount = get_positive_float("Enter the amount: ")
    category = get_non_empty_string("Enter the category: eg. Food, Transport, Entertainment: ")
    description = get_non_empty_string("Enter the description: eg. Lunch at the local cafe: ")
    date = get_date()
    expenses.append(
        {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }
    )

    # naira sign : ₦

    print(f"Expense added: ₦{amount:.2f} in category '{category}' with description '{description}' on {date}.")

def view_expenses(expenses: list) -> None:
    if not expenses:
        print("No expenses recorded.")
        return

    print("\nRecorded Expenses:")
    for idx, expense in enumerate(expenses, start=1):
        print(f"{idx}. Amount: ₦{expense['amount']:.2f}, Category: {expense['category']}, Description: {expense['description']}, Date: {expense['date']}")

def calculate_total(expenses: list) -> float:
    return sum(expense['amount'] for expense in expenses)

def calculate_by_category(expenses: list) -> dict:
    category_totals = {}
    for expense in expenses:
        category_totals[expense['category']] = (
            category_totals.get(expense['category'], 0) + expense['amount']
        )
    return category_totals

def delete_expense(expenses: list) -> None:
    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses(expenses)
    choice = get_valid_int(f"Enter the index of the expense to delete (1-{len(expenses)}, 0 to cancel):", 0, len(expenses))

    if choice == 0:
        print("Delete operation cancelled.")
        return
    
    deleted_expense = expenses.pop(choice-1)
    print(f"Deleted expense: ₦{deleted_expense['amount']:.2f} in category '{deleted_expense['category']}' with description '{deleted_expense['description']}' on {deleted_expense['date']}")

def has_unsaved_changes() -> bool:
    return expenses != last_saved

def save_to_JSON():
    global last_saved
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4)
        print(f"Expenses saved to {DATA_FILE}")
        last_saved = [expense.copy() for expense in expenses]
    except (PermissionError, OSError) as e:
        print(f"Error saving expenses: {e}")

def load_from_JSON():
    global expenses, last_saved
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except FileNotFoundError:
        print("No existing expenses found. Starting fresh.")
        return
    except (json.JSONDecodeError, PermissionError, OSError) as e:
        print(f"Error loading expenses: {e}")
        return

    if has_unsaved_changes():
        answer = input(f"You have {len(expenses)} unsaved expense(s). Do you want to overwrite them with the loaded expenses? (y/n): ").strip().lower()
        if answer != 'y':
            print("load cancelled. Keeping current expenses.")
            return

    expenses = loaded
    last_saved = [expense.copy() for expense in expenses]
    print(f"Loaded {len(expenses)} expense(s) from {DATA_FILE}")


def show_menu():
    print("""
========= EXPENSE TRACKER MENU =========
1. Add Expense
2. View Expenses
3. Total Spending
4. Spending by Category
5. Delete Expense
6. Save Expenses
7. Load Expenses
8. Exit
""")

def main():
    load_from_JSON()
    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if not expenses and choice in ('2', '3', '4', '5'):
            print("No expenses found. Add expense (option 1) or load a saved file (option 7).")
            continue

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            total = calculate_total(expenses)
            print(f"Total spending: ₦{total:.2f}")
        elif choice == '4':
            category_totals = calculate_by_category(expenses)
            print("Spending by Category:")
            for category, total in category_totals.items():
                print(f"{category}: ₦{total:.2f}")
        elif choice == '5':
            delete_expense(expenses)
        elif choice == '6':
            save_to_JSON()
        elif choice == '7':
            load_from_JSON()
        elif choice == '8':
            if expenses:
                save_choice = input("Do you want to save your expenses before exiting? (y/n): ").strip().lower()
                if save_choice == 'y':
                    save_to_JSON()
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
