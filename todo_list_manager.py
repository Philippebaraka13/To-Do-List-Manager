import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

# Task Manager Class
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")

        self.tasks = []
        self.file_name = "tasks.json"

        # Load tasks from file
        self.load_tasks()

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Task List Display
        self.task_listbox = tk.Listbox(self.root, height=10, width=50)
        self.task_listbox.grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, sticky="ew")

        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=1, column=1, sticky="ew")

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, sticky="ew")

        self.sort_priority_button = tk.Button(self.root, text="Sort by Priority", command=self.sort_by_priority)
        self.sort_priority_button.grid(row=2, column=1, sticky="ew")

        self.sort_deadline_button = tk.Button(self.root, text="Sort by Deadline", command=self.sort_by_deadline)
        self.sort_deadline_button.grid(row=3, column=0, sticky="ew")

        self.save_button = tk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=3, column=1, sticky="ew")

        # Update task list display
        self.update_task_list()

    def add_task(self):
        task_name = simpledialog.askstring("Input", "Task Name:")
        if not task_name:
            return

        deadline = simpledialog.askstring("Input", "Deadline (YYYY-MM-DD):")
        if not deadline:
            return

        category = simpledialog.askstring("Input", "Category:")
        if not category:
            return

        priority = simpledialog.askinteger("Input", "Priority (1-5):")
        if not priority:
            return

        task = {
            "name": task_name,
            "deadline": deadline,
            "category": category,
            "priority": priority
        }

        self.tasks.append(task)
        self.update_task_list()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to edit.")
            return

        index = selected_index[0]
        task = self.tasks[index]

        new_name = simpledialog.askstring("Edit Task", "New Task Name:", initialvalue=task["name"])
        new_deadline = simpledialog.askstring("Edit Task", "New Deadline (YYYY-MM-DD):", initialvalue=task["deadline"])
        new_category = simpledialog.askstring("Edit Task", "New Category:", initialvalue=task["category"])
        new_priority = simpledialog.askinteger("Edit Task", "New Priority (1-5):", initialvalue=task["priority"])

        task["name"] = new_name
        task["deadline"] = new_deadline
        task["category"] = new_category
        task["priority"] = new_priority

        self.update_task_list()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return

        index = selected_index[0]
        del self.tasks[index]
        self.update_task_list()

    def sort_by_priority(self):
        self.tasks.sort(key=lambda task: task["priority"])
        self.update_task_list()

    def sort_by_deadline(self):
        self.tasks.sort(key=lambda task: datetime.strptime(task["deadline"], "%Y-%m-%d"))
        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_str = f"{task['name']} - {task['category']} - Due: {task['deadline']} - Priority: {task['priority']}"
            self.task_listbox.insert(tk.END, task_str)

    def save_tasks(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.tasks, file)
        messagebox.showinfo("Save Tasks", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open(self.file_name, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
