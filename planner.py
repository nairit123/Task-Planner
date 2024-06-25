import pickle
import os
import datetime
import threading
import time
import subprocess

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

# Update existing tasks and reminders to have the new fields if they don't have them
def update_structure():
    global tasks, reminders
    for i in range(len(tasks)):
        if len(tasks[i]) == 3:
            tasks[i].extend(["General", "none", []])  # Adding default values for new fields
    for i in range(len(reminders)):
        if len(reminders[i]) == 1:
            reminders[i].extend([None, []])  # Adding default values for new fields
    save_data("tasks.pkl", tasks)
    save_data("reminders.pkl", reminders)

update_structure()

# Background thread for handling reminders
def reminder_thread():
    while True:
        now = datetime.datetime.now()
        for task in tasks:
            task_name, deadline, priority, category, recurring, reminder_times = task
            if deadline and deadline <= now:
                continue  # Skip past deadlines
            for reminder_time in reminder_times:
                reminder_datetime = deadline - reminder_time
                if now >= reminder_datetime and now <= deadline:
                    subprocess.Popen(['notify-send', f'Reminder: {task_name} due on {deadline}'])
                    time.sleep(60)
        for reminder in reminders:
            reminder_text, reminder_deadline, reminder_times = reminder
            if reminder_deadline and reminder_deadline <= now:
                continue  # Skip past deadlines
            for reminder_time in reminder_times:
                reminder_datetime = reminder_deadline - reminder_time
                if now >= reminder_datetime and now <= reminder_deadline:
                    subprocess.Popen(['notify-send', f'Reminder: {reminder_text} due on {reminder_deadline}'])
                    time.sleep(60)
        time.sleep(60)

thread = threading.Thread(target=reminder_thread)
thread.daemon = True
thread.start()

def get_datetime():
    datetime_inp = input("Enter the date and time (MM/DD/YYYY HH:MM): ")
    try:
        dt = datetime.datetime.strptime(datetime_inp, "%m/%d/%Y %H:%M")
    except ValueError:
        print("Sorry, that date/time is in an incorrect format. Try again!")
        return get_datetime()
    return dt

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

def get_category():
    category = input("Enter the category (e.g., Work, Personal, Urgent): ")
    return category

def get_reminder_times():
    reminder_times = []
    while True:
        reminder_time_inp = input("Enter reminder time before deadline (e.g., 1d for 1 day, 2h for 2 hours) or 'done' to finish: ")
        if reminder_time_inp.lower() == 'done':
            break
        try:
            if reminder_time_inp.endswith('d'):
                days = int(reminder_time_inp[:-1])
                reminder_times.append(datetime.timedelta(days=days))
            elif reminder_time_inp.endswith('h'):
                hours = int(reminder_time_inp[:-1])
                reminder_times.append(datetime.timedelta(hours=hours))
            elif reminder_time_inp.endswith('m'):
                minutes = int(reminder_time_inp[:-1])
                reminder_times.append(datetime.timedelta(minutes=minutes))
            else:
                print("Invalid format. Please enter in the format '1d', '2h', or '30m'.")
        except ValueError:
            print("Invalid time. Try again.")
    return reminder_times

def get_recurring():
    recurring = input("Is this a recurring task? (daily, weekly, monthly, none): ").strip().lower()
    if recurring not in ["daily", "weekly", "monthly", "none"]:
        print("Invalid input. Please enter 'daily', 'weekly', 'monthly', or 'none'.")
        return get_recurring()
    return recurring

def task_to_str(task):
    # task = [name: str, deadline: datetime, priority: int, category: str, recurring: str, reminder_times: list]
    return f"{task[0]}: deadline is {task[1].strftime('%m/%d/%Y %H:%M')} and priority is {task[2]}, category is {task[3]}, recurring: {task[4]}"

def reminder_to_str(reminder):
    # reminder = [text: str, deadline: datetime, reminder_times: list]
    deadline_str = reminder[1].strftime('%m/%d/%Y %H:%M') if reminder[1] else 'No deadline'
    return f"{reminder[0]}: deadline is {deadline_str}"

def print_list(items, item_type):
    print(f"{item_type.capitalize()}:")
    for i, item in enumerate(items, 1):
        if item_type == 'task':
            print(f"{i}: {task_to_str(item)}")
        elif item_type == 'reminder':
            print(f"{i}: {reminder_to_str(item)}")
        else:
            print(f"{i}: {item}")
    if not items:
        print(f"No {item_type}s found.")

def add_item(item_type):
    if item_type == "reminder":
        reminder_text = input("What reminder do you want to add? Please type your reminder below: ")
        reminder_deadline = get_datetime() if input("Does this reminder have a deadline? (y/n): ").strip().lower() == 'y' else None
        reminder_times = get_reminder_times()
        reminders.append([reminder_text, reminder_deadline, reminder_times])
        save_data("reminders.pkl", reminders)
    elif item_type == "note":
        note = input("What note do you want to add? Please type your note below: ")
        notes.append(note)
        save_data("notes.pkl", notes)
    elif item_type == "task":
        task_name = input("What is the name of your task? ")
        deadline = get_datetime()
        priority = get_priority()
        category = get_category()
        recurring = get_recurring()
        reminder_times = get_reminder_times()
        tasks.append([task_name, deadline, priority, category, recurring, reminder_times])
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
        deadline = input("Enter new deadline for the task (MM/DD/YYYY HH:MM, leave blank to keep current): ")
        priority = input("Enter new priority for the task (1-10, leave blank to keep current): ")
        category = input("Enter new category for the task (leave blank to keep current): ")
        recurring = input("Enter new recurring interval for the task (daily, weekly, monthly, none; leave blank to keep current): ")
        reminder_times = input("Enter new reminder times (e.g., 1d, 2h, 30m) or leave blank to keep current: ")

        if task_name:
            task[0] = task_name
        if deadline:
            task[1] = datetime.datetime.strptime(deadline, "%m/%d/%Y %H:%M")
        if priority:
            task[2] = int(priority)
        if category:
            task[3] = category
        if recurring:
            task[4] = recurring
        if reminder_times:
            task[5] = get_reminder_times()

        save_data("tasks.pkl", tasks)
        print("Task updated.")
    else:
        print("Nothing updated.")

def show_commands():
    print("Available commands:")
    print("ra to add reminder")
    print("rv to view reminders")
    print("na to add note")
    print("nv to view notes")
    print("ta to add task")
    print("tv to view tasks")
    print("td to delete task")
    print("tu to update task")
    print("rd to delete reminder")
    print("nd to delete note")

# Main loop
while True:
    command = input("Enter a command (type 'help' for available commands): ").strip().lower()
    if command == 'ra':
        add_item("reminder")
    elif command == 'rv':
        print_list(reminders, "reminder")
    elif command == 'na':
        add_item("note")
    elif command == 'nv':
        print_list(notes, "note")
    elif command == 'ta':
        add_item("task")
    elif command == 'tv':
        print_list(tasks, "task")
    elif command == 'td':
        delete_item("task")
    elif command == 'tu':
        update_task()
    elif command == 'rd':
        delete_item("reminder")
    elif command == 'nd':
        delete_item("note")
    elif command == 'help':
        show_commands()
    elif command == 'exit':
        break
    else:
        print("Unknown command. Type 'help' for available commands.")

