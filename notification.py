import pickle
import os
import datetime
import time

def push(message,title=None,subtitle=None):
    titlePart = ''
    if(not title is None):
        titlePart = 'with title "{0}"'.format(title)
    subtitlePart = ''
    if(not subtitle is None):
        subtitlePart = 'subtitle "{0}"'.format(subtitle)

    appleScriptNotification = 'display notification "{0}" {1} {2}'.format(message,titlePart,subtitlePart)
    os.system("osascript -e '{0}'".format(appleScriptNotification))


# Helper function to load data from pickle files
def load_data(filename, default_value):
    if not os.path.isfile(filename):
        with open(filename, "wb") as f:
            pickle.dump(default_value, f)
    with open(filename, "rb") as f:
        return pickle.load(f)

# Load tasks and reminders
tasks = load_data("tasks.pkl", [])
reminders = load_data("reminders.pkl", [])

def send_notifications():
    while True:
        now = datetime.datetime.now()
        # Check for tasks and send notifications
        for task in tasks:
            task_name, deadline, priority, category, recurring, reminder_times = task
            if deadline and deadline <= now:
                continue  # Skip past deadlines
            for reminder_time in reminder_times:
                reminder_datetime = deadline - reminder_time
                if now >= reminder_datetime and now <= deadline:
                    push(title='Task Reminder',
                         message=f'Reminder: {task_name} due on {deadline}',)
                    time.sleep(50)  # Sleep to avoid repeated notifications
        # Check for reminders and send notifications
        for reminder in reminders:
            reminder_text, reminder_deadline, reminder_times = reminder
            if reminder_deadline and reminder_deadline <= now:
                continue  # Skip past deadlines
            for reminder_time in reminder_times:
                reminder_datetime = reminder_deadline - reminder_time
                if now >= reminder_datetime and now <= reminder_deadline:
                    push(title='Reminder',
                         message=f'Reminder: {reminder_text} due on {reminder_deadline}',)
                    time.sleep(50)  # Sleep to avoid repeated notifications
        time.sleep(50)  # Check every minute

if __name__ == "__main__":
    send_notifications()

