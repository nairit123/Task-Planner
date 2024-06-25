import pickle
import os
import datetime

# Helper function to load data from pickle files
def load_data(filename, default_value):
    if not os.path.isfile(filename):
        with open(filename, "wb") as f:
            pickle.dump(default_value, f)
    with open(filename, "rb") as f:
        return pickle.load(f)

# Helper function to save data to pickle files
def save_data(filename, data):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

# Initialize data files
reminders = load_data("reminders.pkl", [])
notes = load_data("notes.pkl", [])
tasks = load_data("tasks.pkl", [])

def get_date():
    date_inp = input("Enter the date (MM/DD/YYYY): ")
    try:
        date = datetime.datetime.strptime(date_inp, "%m/%d/%Y")
    except ValueError:
        print("Sorry, that date is in an incorrect format. Try again!")
        return get_date()
    return date

def get_priority():
    priority_inp = input("Enter the priority (1-10): ")
    try:
        priority = int(priority_inp)
    except ValueError:
        print("Priority should be an int from 1 to 10 inclusive.")
        return get_priority()
    if priority < 1 or priority > 10:
        print("Priority should be an int from 1 to 10 inclusive.")
        return get_priority()
    return priority

def task_to_str(task):
    # task = [name: str, deadline: datetime, priority: int]
    return f"{task[0]}: deadline is {task[1].strftime('%m/%d/%Y')} and priority is {task[2]}"

def print_list(items, item_type):
    print(f"{item_type.capitalize()}:")
    for i, item in enumerate(items, 1):
        print(f"{i}: {item if item_type != 'task' else task_to_str(item)}")
    if not items:
        print(f"No {item_type}s found.")

def add_item(item_type):
    if item_type == "reminder":
        reminder = input("What reminder do you want to add? Please type your reminder below: ")
        reminders.append(reminder)
        save_data("reminders.pkl", reminders)
    elif item_type == "note":
        note = input("What note do you want to add? Please type your note below: ")
        notes.append(note)
        save_data("notes.pkl", notes)
    elif item_type == "task":
        task_name = input("What is the name of your task? ")
        deadline = get_date()
        priority = get_priority()
        tasks.append([task_name, deadline, priority])
        save_data("tasks.pkl", tasks)

def delete_item(item_type):
    if item_type == "reminder":
        items = reminders
        filename = "reminders.pkl"
    elif item_type == "note":
        items = notes
        filename = "notes.pkl"
    elif item_type == "task":
        items = tasks
        filename = "tasks.pkl"

    print_list(items, item_type)
    try:
        delete = int(input(f"Enter {item_type} # to delete or some other string to not delete anything: "))
    except ValueError:
        delete = -1

    if 1 <= delete <= len(items):
        del items[delete - 1]
        save_data(filename, items)
        print(f"{item_type.capitalize()} deleted.")
    else:
        print("Nothing deleted.")

def update_task():
    print_list(tasks, "task")
    try:
        update = int(input("Enter task # to update or some other string to not update anything: "))
    except ValueError:
        update = -1

    if 1 <= update <= len(tasks):
        task = tasks[update - 1]
        print("Updating task:", task_to_str(task))
        task_name = input("Enter new name for the task (leave blank to keep current): ")
        deadline = input("Enter new deadline for the task (MM/DD/YYYY, leave blank to keep current): ")
        priority = input("Enter new priority for the task (1-10, leave blank to keep current): ")

        if task_name:
            task[0] = task_name
        if deadline:
            task[1] = datetime.datetime.strptime(deadline, "%m/%d/%Y")
        if priority:
            task[2] = int(priority)

        save_data("tasks.pkl", tasks)
        print("Task updated.")
    else:
        print("Nothing updated.")

def show_commands():
    print("Available commands:")
    print("ra to add reminder")
    print("rv to view reminders")
    print("rd to delete reminder")
    print("na to add note")
    print("nv to view notes")
    print("nd to delete note")
    print("ta to add task")
    print("tv to view tasks")
    print("td to delete task")
    print("tu to update task")

firstrun = True

while True:
    if firstrun:
        print("What do you want to do? Type 'c' to view available commands.")
        firstrun = False

    command = input("").strip().lower()
    print("\n")

    if command == "c":
        show_commands()
    elif command == "ra":
        add_item("reminder")
    elif command == "rv":
        print_list(reminders, "reminder")
    elif command == "rd":
        delete_item("reminder")
    elif command == "na":
        add_item("note")
    elif command == "nv":
        print_list(notes, "note")
    elif command == "nd":
        delete_item("note")
    elif command == "ta":
        add_item("task")
    elif command == "tv":
        print_list(tasks, "task")
    elif command == "td":
        delete_item("task")
    elif command == "tu":
        update_task()
    else:
        print("Command invalid, try again.")

    print("\nCommand successful.\n")
