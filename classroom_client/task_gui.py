import base64
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry


from main_client import Client


class TaskWindow:
    def __init__(self, root, course, on_task_created):
        self.root = root
        self.course = course
        self.on_task_created = on_task_created  # Callback function to update tasks
        self.file_data = None  # To store file content
        self.file_path = None  # To store file path
        self.create_task_window()

    def create_task_window(self):
        """Create the task input form."""
        self.task_window = tk.Toplevel(self.root)
        self.task_window.title("Create New Task")
        self.task_window.geometry("400x400")

        tk.Label(self.task_window, text="Task Name:").pack()
        self.task_name_entry = tk.Entry(self.task_window, width=40)
        self.task_name_entry.pack(pady=5)

        tk.Label(self.task_window, text="Due Date:").pack()
        self.due_date_entry = DateEntry(self.task_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.due_date_entry.pack(pady=5)

        tk.Label(self.task_window, text="Description:").pack()
        self.text_entry = tk.Text(self.task_window, height=5, width=40)
        self.text_entry.pack(pady=5)

        tk.Button(self.task_window, text="Attach Document", command=self.upload_file).pack(pady=5)

        self.create_task_button = tk.Button(self.task_window, text="Create Task", command=self.save_task)
        self.create_task_button.pack(pady=10)

    def upload_file(self):
        """Open file dialog and store file content if it's under 16MB."""
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            file_size = len(open(self.file_path, "rb").read())
            if file_size > 16 * 1024 * 1024:  # 16MB limit
                messagebox.showerror("Error", "File size exceeds 16MB limit.")
                return
            with open(self.file_path, "rb") as f:
                self.file_data = base64.b64encode(f.read()).decode('utf-8')
                # Binary(f.read())  # Convert to binary for MongoDB
            messagebox.showinfo("Success", "File uploaded successfully!")

    def save_task(self):
        """Save the task to MongoDB or update UI."""
        task_name = self.task_name_entry.get()
        due_date = self.due_date_entry.get_date()
        description = self.text_entry.get("1.0", tk.END).strip()

        if not task_name:
            messagebox.showerror("Error", "Task name cannot be empty!")
            return


        new_task = {
            "course_id":self.course["_id"],
            "task_name": task_name,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "description": description,
            "file_name": self.file_path.split("/")[-1] if self.file_path else "",  # Extract file name
            "file_data": self.file_data if self.file_data else ""
        }

        dump = json.dumps(new_task)

        client = Client()

        # Connect to the server
        client.connect()
        # First, send the size of the JSON message
        message = f"new_task:{dump}"
        # message_size = str(len(message)).zfill(10)  # Fixed 10-byte size header
        # client.send_message(f"new_task:{message_size.encode('utf-8')}")

        # Now send the actual JSON message
        answer = client.send_message(message.encode("utf-8"))
        print(answer)
        answer = client.send_message(message)
        print(answer)
        client.disconnect()
        # Notify course window that a new task was created
        self.on_task_created(new_task)


        messagebox.showinfo("Success", "Task created successfully!")
        self.task_window.destroy()
