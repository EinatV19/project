import tkinter as tk
from tkinter import messagebox, PhotoImage
from task_gui import TaskWindow  # Import the task creation window
from video.teacher_video_server import TeacherServer


class CourseWindow:
    def __init__(self, root, course, is_teacher):
        self.root = root
        self.course = course
        self.is_teacher = is_teacher  # Store teacher or student mode
        self.server = None  # Will hold the TeacherServer instance
        self.tasks = course.get("tasks", [])  # Load tasks
        self.create_course_window()
    def on_task_button_click(self, task):
        messagebox.showinfo("Task", f"Task: {task['task_name']}")

    def open_task_window(self):
        """Open the task creation window."""
        TaskWindow(self.root, self.course, self.add_new_task)

    def add_new_task(self, new_task):
        """Update task list when a new task is created."""
        self.tasks.append(new_task)
        self.refresh_task_buttons()

    def refresh_task_buttons(self):
        """Refresh task buttons after adding a new task."""
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()  # Clear previous buttons

        for task in self.tasks:
            button = tk.Button(self.tasks_frame, text=task["task_name"],
                               command=lambda t=task: self.on_task_button_click(t),
                               width=20, font=("Arial", 16))
            button.pack(pady=5, fill=tk.X, expand=True)

    def copy_course_id(self):
        """Copy the course ID to the clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.course["id"])
        self.root.update()  # Required to update the clipboard
        messagebox.showinfo("Copied", "Course ID copied to clipboard!")

    def create_course_window(self):
        """Create the course window."""
        self.course_window = tk.Toplevel(self.root)
        self.course_window.title(f"Course {self.course['name']}")
        self.course_window.geometry("800x600")

        # Course ID Label + Copy Button
        course_id_frame = tk.Frame(self.course_window)
        course_id_frame.pack(pady=10)

        course_id_label = tk.Label(course_id_frame, text=f"Course ID: {self.course['_id']}", font=("Arial", 14))
        course_id_label.pack(side=tk.LEFT, padx=10)

        copy_button = tk.Button(course_id_frame, text="📋 Copy", command=self.copy_course_id, font=("Arial", 12))
        copy_button.pack(side=tk.RIGHT)

        # Teacher Only: Start/Stop Streaming
        if self.is_teacher:
            self.start_button = tk.Button(self.course_window, text="Start Streaming", command=self.start_streaming,
                                          width=20, font=("Arial", 16))
            self.start_button.pack(pady=10)

            self.stop_button = tk.Button(self.course_window, text="Stop Streaming", command=self.stop_streaming,
                                         state=tk.DISABLED, width=20, font=("Arial", 16))
            self.stop_button.pack(pady=10)

        # Student Only: Join Streaming Button
        if not self.is_teacher:
            join_streaming_button = tk.Button(self.course_window, text="Join Streaming",
                                              command=self.join_streaming, font=("Arial", 16))
            join_streaming_button.pack(pady=10)

        # Tasks Section
        tasks_section = tk.Frame(self.course_window, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        tasks_section.pack(pady=10, fill=tk.X, expand=True)

        tasks_label = tk.Label(tasks_section, text="Tasks", font=("Arial", 16, "bold"))
        tasks_label.pack()

        self.tasks_frame = tk.Frame(tasks_section)
        self.tasks_frame.pack(pady=10)
        self.refresh_task_buttons()

        # Teacher Only: Create New Task Button
        if self.is_teacher:
            create_task_button = tk.Button(self.course_window, text="Create New Task",
                                           command=self.open_task_window, font=("Arial", 14))
            create_task_button.pack(pady=10)

    def join_streaming(self):
        """Start student client to join the teacher's streaming."""
        from video.student_video_client import student_client  # Import student client
        student_client('127.0.0.1', 9999, 8888)

    def start_streaming(self):
        """Starts the teacher's video & audio streaming server."""
        if not self.server:
            self.server = TeacherServer(server_ip="0.0.0.0", video_port=9999, audio_port=8888)
        self.server.start_server()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_streaming(self):
        """Stops the teacher's video & audio streaming server."""
        if self.server:
            self.server.stop_server()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
