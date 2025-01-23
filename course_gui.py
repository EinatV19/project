import tkinter as tk
from tkinter import messagebox

# Define the list of tasks
tasks = ["\u05de\u05d8\u05dc\u05d4 1", "\u05de\u05d8\u05dc\u05d4 2", "\u05de\u05d8\u05dc\u05d4 3"]

# Function to handle task button click
def on_task_button_click(task_name):
    messagebox.showinfo("Task", f"{task_name}")

# Create the main window
root = tk.Tk()
root.title("Dynamic Task Window")
root.attributes('-fullscreen', True)  # Set the window to fullscreen

# Add the class name label
class_label = tk.Label(root, text="\u05de\u05d3\u05e2\u05d9 \u05d4\u05de\u05d7\u05e9\u05d1 \u05d9\u05d04", font=("Arial", 24))
class_label.pack(pady=20)

# Frame for tasks buttons
tasks_frame = tk.Frame(root)
tasks_frame.pack(pady=20)

# Create a button for each task
def create_task_buttons():
    for task in tasks:
        button = tk.Button(tasks_frame, text=task, command=lambda t=task: on_task_button_click(t), width=20, font=("Arial", 16))
        button.pack(pady=10, fill=tk.X, expand=True)

create_task_buttons()

# Add the camera button
camera_icon = tk.PhotoImage(file="camera.png")  # Load the camera image
camera_button = tk.Button(root, image=camera_icon, borderwidth=0)
camera_button.place(relx=0.95, rely=0.05, anchor="ne")  # Place it in the top-right corner

# Run the Tkinter event loop
root.mainloop()
