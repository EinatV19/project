import json
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox, PhotoImage
from task_gui import TaskWindow  # Import the task creation window
from video.teacher_video_server import TeacherServer


class ViewTaskWindow:
    def __init__(self, root, course, is_teacher,client,task_name):
        self.root = root
        self.course = course
        self.task_name = task_name
        self.is_teacher = is_teacher  # Store teacher or student mode
        self.client = client  # Will hold the TeacherServer instance
        self.create_task_window()

    def create_task_window(self):
        """Create the Task window."""
        self.task_window = tk.Toplevel(self.root)
        self.task_window.title(f"Task {self.task_name}")
        self.task_window.geometry("800x600")

        # Task Download + Upload Buttons
        task_frame = tk.Frame(self.task_window)
        task_frame.pack(pady=10)

        download_button = tk.Button(task_frame, text="Download", command=self.download_task, font=("Arial", 12))
        download_button.pack(side=tk.RIGHT)

        upload_button = tk.Button(task_frame, text="Upload", command=self.upload_task, font=("Arial", 12))
        upload_button.pack(side=tk.LEFT)

    def download_task(self):
        task_details = {"task_name":self.task_name,"course_id":self.course["_id"]}
        file_size_string = self.client.send_message(f"download_task:{json.dumps(task_details)}")
        save_location = tk.filedialog.asksaveasfilename()
        self.client.receive_file(int(file_size_string),save_location)

    def upload_task(self):
        return
