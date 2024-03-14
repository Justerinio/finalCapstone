"""This code provides a basic task manager application with 
functionalities for user registration, task management,
report generation, and statistics display."""


""" os - Module for interacting with the operating system, used for 
file operations.
datetime - Module for working with dates and times, used for handling
task due dates and generating reports."""

import os
from datetime import datetime


def login():
    """
    Authenticates users by verifying their username and password.
    If the entered credentials match, it prints a successful login message.
    """
    # Check if user.txt file exists, if not, create it with default admin credentials
    if not os.path.exists('user.txt'):
        with open('user.txt', "w") as default_file:
            default_file.write("admin,admin\n")

    # Read existing user data from user.txt and store it in a dictionary
    with open('user.txt', 'r') as user_file:
        user_data = user_file.read().splitlines()

    username_password = {}
    for user in user_data:
        username, password = user.split(',')
        username_password[username] = password

    # Continuously prompt the user for credentials until a valid match is found
    while True:
        print("\n=== LOGIN ===")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        if curr_user not in username_password:
            print("User not taken.")
        elif username_password[curr_user] != curr_pass:
            print("Incorrect password.")
        else:
            print("Login successful!")
            return curr_user


def reg_user():
    """
    Allows the user to register by entering a new username and password.
    It checks if the user.txt file exists, reads existing usernames,
    ensures the entered username is unique, and appends the new user to user.txt.
    """
    # Prompt user to enter a new username
    username = input("Enter a new username: ")

    # Check if user.txt file exists; if not, create it
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as file:
            pass
    
    # Check if the entered username already exists in the user.txt file  
    with open("user.txt", "r") as file:
        for line in file:
            existing_username = line.split(",")[0].strip()
            if username == existing_username:
                print("Username already exists.Please choose a different one.")
                return
    
    # Prompt user to enter a password  
    password = input("Enter a password: ")

    # Append the new username and password to the user.txt file  
    with open("user.txt", "a") as file:
        file.write(f"{username},{password}\n")
    
    # Print a success message after user registration
    print("User registered successfully!")


def add_task():
    """
    Allows the user to add a new task by providing task details.
    It prompts the user for the username, task title, description,
    due date, and assigns the current date as the date assigned.
    It appends the task details to the 'tasks.txt' file.
    """
    # Prompt user for the username of the person the task is assigned to
    username = input("Enter the username of the "
                     "person the task is assigned to: ")
    
    # Prompt user for the title of the task
    title = input("Enter the title of the task: ")

    # Prompt user for the description of the task
    description = input("Enter a description of the task: ")

    # Get the current date and format it as YYYY-MM-DD
    date_assigned = datetime.today().strftime('%Y-%m-%d')

     # Prompt user for the due date of the task
    due_date = input("Enter the due date of the task (YYYY-MM-DD): ")

    # Initialize the task as not completed
    completed = "No"

    # Append the task details to the 'tasks.txt' file
    with open("tasks.txt", "a") as file:
        file.write(username + "," + title + "," + description + 
                   "," + date_assigned + "," + due_date + "," + 
                   completed +"\n")
        
    # Print a success message after adding the task
    print("Task added successfully!")


def view_all():
    """
    Displays all tasks stored in the tasks.txt file.
    It reads tasks from the file and prints each task with its corresponding index.
    """

    # Print header for the task display
    print("\n=== All Tasks ===\n")

    # Open tasks.txt file for reading
    with open("tasks.txt", "r") as file:

        # Read all lines from the file and store them in a list
        tasks = file.readlines()

        # Check if there are tasks in the file
        if tasks:

            # Iterate over each task in the tasks list with its index
            for i, task in enumerate(tasks, 1):

                # Split the task data into individual components
                task_data = task.strip().split(",")
                username, title, description, assigned_date, due_date, completed = task_data

                # Print task details in a readable manner
                print('-' * 30)
                print(f"Task {i}:")
                print(f"Title: {title}")
                print(f"Assigned to: {username}")
                print(f"Description: {description}")
                print(f"Date Assigned: {assigned_date}")
                print(f"Due Date: {due_date}")
                print(f"Completed: {'Yes' if completed.lower() == 'yes' else 'No'}")
                print("-" * 30)
        else:

            # If no tasks are found, print a message
            print("No tasks found.")


def view_mine(curr_user):
    """
    Displays tasks assigned to the currently logged-in user.
    It reads tasks from tasks.txt, filters tasks based on the entered username,
    and displays them with options to edit or mark tasks as complete.
    """

    # Open tasks.txt file for reading
    with open("tasks.txt", "r") as file:

        # Read all lines from the file and store them in a list
        tasks = file.readlines()

    # Initialize an empty list to store tasks assigned to the current user
    user_tasks = []

    # Iterate through each task in the tasks list
    for task in tasks:

        # Check if the task is assigned to the current user
        if task.startswith(curr_user):

            # Split the task data into individual components and append to user_tasks list
            user_task = task.strip().split(",")
            user_tasks.append(user_task)

    # Check if there are tasks assigned to the current user
    if not user_tasks:
        print("No tasks assigned to you.")
        return

    # Print header for the user's tasks
    print("\n=== Your Tasks ===\n")

    # Iterate through each task assigned to the user with its index
    for i, task in enumerate(user_tasks, 1):

        # Print task details
        print("-" * 30)
        print(f"Task {i}:")
        print(f"Title: {task[1]}")
        print(f"Description: {task[2]}")
        print(f"Date Assigned: {task[3]}")
        print(f"Due Date: {task[4]}")
        print(f"Completed: {'Yes' if task[5].lower() == 'yes' else 'No'}")
        print("-" * 30)

    # Prompt the user to choose a task to edit or mark as complete
    task_choice = input("Enter the number of the task you want to edit "
                        "or mark as complete (-1 to return): ")
    
    # Check if the user wants to return to the main menu
    if task_choice == '-1':
        print("Returning to main menu.")
        return

    try:
        # Convert the user input to an integer
        task_choice = int(task_choice)

        # Get the selected task from the user_tasks list
        selected_task = user_tasks[task_choice - 1]
        if selected_task[5].lower() == "yes":
            print("This task has already been completed and cannot "
                  "be edited.")
            return

        # Prompt the user to choose an action for the selected task
        action = input("Do you want to mark this task as complete "
                       "(enter 'mark') or edit it (enter 'edit'): ")
        
        # Process the user's action choice
        if action.lower() == "mark":
            selected_task[5] = "Yes"
        elif action.lower() == "edit":
            new_username = input("Enter new username "
                                 "(leave blank to keep the same): ")
            new_due_date = input("Enter new due date (YYYY-MM-DD, "
                                 "leave blank to keep the same): ")
            if new_username:
                selected_task[0] = new_username
            if new_due_date:
                selected_task[4] = new_due_date
        else:
            print("Invalid choice.")
            return

        # Write the updated tasks to a temporary file
        with open("tasks_temp.txt", "w") as file:
            for task in tasks:
                if task.strip().split(",")[1] != selected_task[1]:
                    file.write(task)
                else:
                    file.write(','.join(selected_task) + '\n')

        # Replace the original tasks file with the temporary file
        os.replace("tasks_temp.txt", "tasks.txt")

        # Print a message based on the action performed
        if action.lower() == "mark":
            print("Task marked as complete.")
        elif action.lower() == "edit":
            print("Task edited successfully.")

    except (ValueError, IndexError):
        print("Invalid input or task number.")
        return


def generate_reports():
    """
    Generates task and user overview reports.
    Calculates statistics such as total tasks, completed tasks,
    uncompleted tasks, overdue tasks, and percentages.
    Writes the calculated statistics to task_overview.txt and user_overview.txt files.
    """
    try:

        # Open tasks.txt file for reading
        with open("tasks.txt", "r") as tasks_file:

            # Read all lines from the file and store them in a list
            tasks = tasks_file.readlines()

            # Calculate total number of tasks
            total_tasks = len(tasks)

            # Count completed tasks
            completed_tasks = sum(1 for task in tasks if task.strip().split(",")[-1].lower() == "yes")
            
            # Calculate number of uncompleted tasks
            uncompleted_tasks = total_tasks - completed_tasks

            # Count overdue tasks
            overdue_tasks = sum(1 for task in tasks if datetime.strptime(task.strip().split(",")[-2].strip(),
                                "%Y-%m-%d").date() < datetime.now().date())
            
            # Calculate percentages
            incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
            overdue_percentage = (overdue_tasks / total_tasks) * 100

        # Write task overview report to task_overview.txt
        with open("task_overview.txt", "w") as report_file:
            report_file.write(f"Total tasks: {total_tasks}\n")
            report_file.write(f"Completed tasks: {completed_tasks}\n")
            report_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
            report_file.write(f"Overdue tasks: {overdue_tasks}\n")
            report_file.write(f"""Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n""")
            report_file.write(f"""Percentage of overdue tasks: {overdue_percentage:.2f}%\n""")
    except ZeroDivisionError:

        # If no tasks are found, write a message to task_overview.txt
        with open("task_overview.txt", "w") as report_file:
            report_file.write("No tasks found.\n")

    try:

        # Open user.txt file for reading
        with open("user.txt", "r") as users_file:

            # Read all lines from the file and store them in a list
            users = users_file.readlines()

        # Calculate total number of users
        total_users = len(users)
        user_overview = []

        # Iterate through each user in the users list
        for user in users:

            # Extract username from each line
            username = user.strip().split(",")[0]

            # Filter tasks assigned to the current user
            user_tasks = [task.strip().split(",") for task in tasks if task.startswith(username)]
            
            # Count total tasks assigned to the user
            total_user_tasks = len(user_tasks)

            # Count completed tasks for the user
            completed_user_tasks = sum(1 for task in user_tasks if task[-1].lower() == "yes")
            
            # Calculate number of uncompleted tasks for the user
            uncompleted_user_tasks = total_user_tasks - completed_user_tasks

            # Count overdue tasks for the user
            overdue_user_tasks = sum(1 for task in user_tasks if datetime.strptime(task[-2].strip(),
                                    "%Y-%m-%d").date() < datetime.now().date())

            # Calculate percentages for the user
            incomplete_user_percentage = 0
            overdue_user_percentage = 0
            if total_user_tasks != 0:
                incomplete_user_percentage = (uncompleted_user_tasks / total_user_tasks) * 100
                overdue_user_percentage = (overdue_user_tasks / total_user_tasks) * 100
            
            # Append user data to user_overview list
            user_overview.append((username, total_user_tasks,
                                    completed_user_tasks,
                                    uncompleted_user_tasks,
                                    overdue_user_tasks,
                                    incomplete_user_percentage,
                                    overdue_user_percentage))

        # Write user overview report to user_overview.txt
        with open("user_overview.txt", "w") as report_file:
            report_file.write(f"Total users: {total_users}\n")
            for user_data in user_overview:
                report_file.write(f"User: {user_data[0]}\n")
                report_file.write(f"Total tasks: {user_data[1]}\n")
                report_file.write(f"Completed tasks: {user_data[2]}\n")
                report_file.write(f"Uncompleted tasks: {user_data[3]}\n")
                report_file.write(f"Overdue tasks: {user_data[4]}\n")
                report_file.write(f"""Percentage of incomplete tasks: {user_data[5]:.2f}%\n""")
                report_file.write(f"""Percentage of overdue tasks: {user_data[6]:.2f}%\n""")
                report_file.write("\n")
    except ZeroDivisionError:

        # If no users are found, write a message to user_overview.txt
        with open("user_overview.txt", "w") as report_file:
            report_file.write("No users found.\n")


def display_statistics():
    """
    Displays statistics from the generated reports.
    If the report files do not exist, it calls generate_reports() to create them.
    It reads the report files and prints the statistics.
    """

    # Check if the task overview or user overview report files do not exist
    if not os.path.exists("task_overview.txt") or \
        not os.path.exists("user_overview.txt"):

        # Call generate_reports() function to create the reports
        generate_reports()

    # Open and print the content of the task overview report file
    with open("task_overview.txt", "r") as file:
        print(file.read())

    # Open and print the content of the user overview report file
    with open("user_overview.txt", "r") as file:
        print(file.read())


def main():
    """
    Main entry point of the program.
    Displays the menu options and prompts the user to select an action.
    Based on the user's choice, it calls the corresponding function to perform the action.
    """
    curr_user = login()
    while True:
        print("\n===== Task Manager Menu =====")
        print("r - Register User")
        print("a - Add Task")
        print("va - View All Tasks")
        print("vm - View My Tasks")
        print("gr - Generate Reports")
        print("ds - Display Statistics")
        print("e - Exit")

        choice = input("Enter your choice: ")

        if choice == "r":
            reg_user()
        elif choice == "a":
            add_task()
        elif choice == "va":
            view_all()
        elif choice == "vm":
            view_mine(curr_user)
        elif choice == "gr":
            generate_reports()
            print("Reports generated successfully.")
        elif choice == "ds":
            display_statistics()
        elif choice == "e":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
