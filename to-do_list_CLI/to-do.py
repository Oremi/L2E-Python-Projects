import datetime
import itertools

italic_start = "\033[3m"
reset = "\033[0m"

tasks = []

task_id_counter = itertools.count(start=1) # Unique task ID generator

def clear_screen():
    print("\033[H\033[J", end="")

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

def add_task():
    while True:
        clear_screen()
        print("Add a New Task")
        title =  get_non_empty_string("Enter the task title: ")
        task_id = next(task_id_counter)
        task = {
            "id": task_id,
            "title": title,
            "completed": False,
            "due_date": "",
            "priority": "",
            "created_at": get_date()
        }
        tasks.append(task)
        print(f"\n Success: Task '{title}' added with ID #{task_id}!")

        # again = (input("\nDo you want to add another task? (y/n): ").strip().lower())

        # if again != 'yes' or 'y':
        #     break

def view_tasks():
    if not tasks:
        print("no tasks available.")
        print(f"You can add a new task by selecting the {italic_start}Add Task'{reset} option.")
        return
    else:
        print("\nCurrent Tasks:")
        for task in tasks:
            status = "Completed" if task["completed"] else "Pending"
            print(f"#{task['id']}. Title: {task['title']}, Status: {status}, Created At: {task['created_at']}")

def mark_completed():
    if not tasks:
        print("No tasks available to mark as completed.")
        return
    else:
        view_tasks()
        task_id = get_positive_int(f"\nEnter the task ID to mark as {italic_start}completed{reset}: ")

        # get unique ID
        task_to_update = next(
            (task for task in tasks if task["id"] == task_id), None
        )
        if task_to_update:
            task_to_update["completed"] = True
            print(f"Task Completed: #{task_to_update['id']}. {task_to_update['title']}")
        else:
            print(f"Error: Task with ID {task_id} not found.")

def main():
    while True:
        clear_screen()
        print("To-Do List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
            input("\nPress Enter to return to the main menu...")
        elif choice == "3":
            mark_completed()
            input("\nPress Enter to return to the main menu...")
        elif choice == "4":
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please select a number between 1 and 4.")
            input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()