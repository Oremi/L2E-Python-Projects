import datetime
import json
import os

# Terminal Formatting Codes
italic_start = "\033[3m"
reset = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"

TASKS_FILE = "todo_tasks.json"
tasks = []

# task_id_counter = itertools.count(start=1) # Unique task ID generator

def clear_screen():
    print("\033[H\033[J", end="")

def load_task():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as file:
                tasks = json.load(file)
        except json.JSONDecodeError:
            print("Warning: Tasks file was corrupted. Starting fresh.")
            tasks = []
    else:
        tasks = []

def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)
        print(f"Tasks saved to {TASKS_FILE}")

def reorder_ids():
    """Re-indexes task IDs sequentially starting from 1 and saves the updates."""
    for index, task in enumerate(tasks, start=1):
        task["id"] = index
    save_tasks()

def get_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty. Please try again.")
            continue
        return value

def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def get_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_validated_due_date(prompt: str, default : str = "") -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            return default  # No due date assigned
        try:
            # Validate correct layout
            valid_date = datetime.datetime.strptime(value, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print(f"Invalid format. Please use YYYY-MM-DD (e.g., {italic_start}2026-12-31){reset}.")

def get_validated_priority(prompt: str, default: str = "None") -> str:
    valid_priorities = {"1": "High", "2": "Medium", "3": "Low", "4": "None"}
    while True:
        print("\nPriority Levels:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        print("4. None")

        choice = input(prompt).strip()

        if choice in valid_priorities:
            return valid_priorities[choice]
        print("Invalid choice. Please select a number between 1 and 4.")


def get_priority_colored(priority: str) -> str:
    if priority == "High":
        return f"{RED}{BOLD}High{reset}"
    elif priority == "Medium":
        return f"{YELLOW}Medium{reset}"
    elif priority == "Low":
        return f"{GREEN}Low{reset}"
    return "None"

def add_task():
    while True:
        clear_screen()
        print("Add a New Task")
        title =  get_non_empty_string("Enter the task title: ")
        due_date = get_validated_due_date("Enter due date (YYYY-MM-DD) or press Enter to skip: ")
        priority = get_validated_priority("Select task priority level (1-4): ")

        task_id = len(tasks) + 1

        task = {
            "id": task_id,
            "title": title,
            "completed": False,
            "due_date": due_date,
            "priority": priority,
            "created_at": get_date()
        }
        tasks.append(task)
        save_tasks()
        print(f"\n Success: Task '{title}' added with ID #{task_id}!")

        again = (input("\nDo you want to add another task? (y/n): ").strip().lower())

        if again not in ('y','yes'):
            break


def view_tasks(filtered_list=None) -> bool:
    target_list = tasks if filtered_list is None else filtered_list

    if not target_list:
        print("No tasks available.")
        return False

    print(f"\n{BOLD}{'ID':<5} {'Title':<25} {'Status':<12} {'Priority':<15} {'Due Date':<12}{reset}")
    print("-" * 75)
    
    for task in target_list:
        status = f"{GREEN}Completed{reset}" if task["completed"] else f"{BLUE}Pending{reset}"
        priority_str = get_priority_colored(task["priority"])
        due = task["due_date"] if task["due_date"] else "N/A"
        
        print(f"#{task['id']:<4} {task['title']:<25} {status:<21} {priority_str:<24} {due:<12}")
    return True

def filter_menu():
    # Sub-menu to filter tasks.
    if not tasks:
        print("No tasks available to filter.")
        return

    while True:
        clear_screen()
        print("Filter View Options")
        print("1. View Pending Tasks Only")
        print("2. View Completed Tasks Only")
        print("3. View High Priority Tasks Only")
        print("4. View All Tasks")
        print("5. Back to Main Menu")

        choice = input("Select a filter option (1-5): ").strip()

        if choice == "1":
            pending = [task for task in tasks if not task["completed"]]
            print("\n--- Pending Tasks ---")
            view_tasks(pending)
            input("\nPress Enter to return to filter menu...")
        elif choice == "2":
            completed = [task for task in tasks if task["completed"]]
            print("\n--- Completed Tasks ---")
            view_tasks(completed)
            input("\nPress Enter to return to filter menu...")
        elif choice == "3":
            high_prio = [task for task in tasks if task["priority"] == "High"]
            print("\n--- High Priority Tasks ---")
            view_tasks(high_prio)
            input("\nPress Enter to return to filter menu...")
        elif choice == "4":
            print("\n--- All System Tasks ---")
            view_tasks()
            input("\nPress Enter to return to filter menu...")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Select a number between 1 and 5.")
            input("\nPress Enter to continue...")

def edit_task():
    # Finds a task by ID
    if not tasks:
        print("No tasks available.")
        print(f"You can add a new task by selecting the {italic_start}Add Task{reset} option.")
        return

    view_tasks()
    task_id = get_positive_int("\nEnter the task ID you want to edit: ")

    task = next((task for task in tasks if task["id"] == task_id), None)

    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    clear_screen()
    print(f"--- Editing Task #{task['id']} ---")
    print(f"Current Title: {task['title']}")
    new_title = input("Enter new title (or press Enter to skip): ").strip()
    if new_title:
        task["title"] = new_title

    print(f"\nCurrent Due Date: {task['due_date'] if task['due_date'] else 'N/A'}")
    task["due_date"] = get_validated_due_date("Enter new due date (YYYY-MM-DD) or press Enter to skip: ", default=task["due_date"])

    print(f"\nCurrent Priority: {task['priority']}")
    task["priority"] = get_validated_priority("Select new priority level (1-4): ", default=task["priority"])

    save_tasks()
    print(f"\nSuccess: Task #{task_id} has been updated successfully!")

def delete_task():
    if not tasks:
        print("no tasks available.")
        return
    else:
        view_tasks()
        task_id = get_positive_int(f"\nEnter the task ID to {italic_start}delete{reset}: ")

        # Safely find the item index matching the target ID
        task_index = next(
        (i for i, task in enumerate(tasks) if task["id"] == task_id), None
        )

        if task_index is not None:
            deleted_task = tasks.pop(task_index)
            print(f"Deleted the task: {deleted_task['title']} at {get_date()}")
            reorder_ids()  # Sequentially updates remaining IDs and saves file
        else:
            print(f"Error: Task with ID {task_id} not found.")


def mark_completed():
    if not tasks:
        print("No tasks available to mark as completed.")
        return
    
    view_tasks()
    task_id = get_positive_int(f"\nEnter the task ID to mark as {italic_start}completed{reset}: ")

    # get unique ID
    task_to_update = next(
        (task for task in tasks if task["id"] == task_id), None
    )

    if task_to_update:
        task_to_update["completed"] = True
        save_tasks()
        print(f"Task Completed: #{task_to_update['id']}. {task_to_update['title']}")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def main():
    load_task()
    while True:
        clear_screen()
        print("To-Do List Application")
        print("1. Add Task")
        print("2. View / Filter Tasks")
        print("3. Edit a Task")
        print("4. Delete a Task")
        print("5. Mark Task as Completed")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            if tasks:
                filter_menu()
            else:
                print("No task available")
                print(f"You can add a new task by selecting the {italic_start}Add Task{reset} option.")
                input("\nPress Enter to return to the main menu...")
        elif choice == "3":
            edit_task()
            input("\nPress Enter to return to the main menu...")
        elif choice == "4":
            delete_task()
            input("\nPress Enter to return to the main menu...")
        elif choice == "5":
            mark_completed()
            input("\nPress Enter to return to the main menu...")
        elif choice == "6":
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please select a number between 1 and 5.")
            input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()