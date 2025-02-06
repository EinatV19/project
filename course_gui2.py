import tkinter as tk
from tkinter import messagebox


class CourseWindow:
    def __init__(self, root, course_id):
        # Initialize the main window and course_id
        self.root = root
        self.course_id = course_id
        self.tasks = ["\u05de\u05d8\u05dc\u05d4 1", "\u05de\u05d8\u05dc\u05d4 2", "\u05de\u05d8\u05dc\u05d4 3"]

        # Create and configure the course window
        self.create_course_window()

    def on_task_button_click(self, task_name):
        # Handle task button click
        messagebox.showinfo("Task", f"{task_name}")

    def create_course_window(self):
        # Create the main window for the course
        self.course_window = tk.Toplevel(self.root)  # Use Toplevel to create a new window
        self.course_window.title(f"Course {self.course_id}")

        # Resize the window with geometry (width x height)
        self.course_window.geometry("800x600")  # Set the window size to 800x600 pixels

        # Add the course label
        class_label = tk.Label(self.course_window,
                               text=f"\u05de\u05d3\u05e2\u05d9 \u05d4\u05de\u05d7\u05e9\u05d1 \u05d9\u05d04 - Course ID: {self.course_id}",
                               font=("Arial", 24))
        class_label.pack(pady=20)

        # Frame for task buttons
        tasks_frame = tk.Frame(self.course_window)
        tasks_frame.pack(pady=20)

        # Create a button for each task
        for task in self.tasks:
            button = tk.Button(tasks_frame, text=task, command=lambda t=task: self.on_task_button_click(t), width=20,
                               font=("Arial", 16))
            button.pack(pady=10, fill=tk.X, expand=True)

        # Add the camera button
        camera_icon = tk.PhotoImage(file="camera.png")  # Load the camera image
        camera_button = tk.Button(self.course_window, image=camera_icon, borderwidth=0)
        camera_button.place(relx=0.95, rely=0.05, anchor="ne")  # Place it in the top-right corner

        # Store the reference to the camera icon to prevent it from being garbage collected
        self.camera_icon = camera_icon
