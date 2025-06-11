import json
import tkinter as tk
from tkinter import messagebox
# from classroom_server.database import delete_course
from classroom_client.course_gui import CourseWindow
from main_client import Client

# client = Client()
# client.connect()
def open_courses_window(root, courses_data, mail, client):
    """Opens the courses window and displays courses where the user is a teacher or student."""
    global courses_window

    if 'courses_window' in globals() and courses_window:
        try:
            if courses_window.winfo_exists():
                courses_window.destroy()
        except:
            pass

    courses_window = tk.Toplevel(root)
    courses_window.title("בחר כיתה")
    courses_window.geometry("800x600")

    label_courses = tk.Label(courses_window, text="בחר כיתה", font=("Arial", 20))
    label_courses.pack(pady=10)

    teacher_courses = courses_data.get('teacher_courses', [])
    student_courses = courses_data.get('student_courses', [])

    # ✅ Teacher Courses Section
    if teacher_courses:
        teacher_frame = tk.Frame(courses_window, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#d1f2eb")  # Light green
        teacher_frame.pack(pady=10, fill=tk.X, expand=True)

        tk.Label(teacher_frame, text="My Courses as Teacher", font=("Arial", 16, "bold"), bg="#d1f2eb").pack()

        def handle_delete_course(course):
            confirm = messagebox.askyesno("Delete Course", f"Are you sure you want to delete {course['name']}?")
            if confirm:
                # result = delete_course(course["id"])
                course_id = course["_id"]
                message = f"delete_course:{course_id}"
                msg = client.send_message(message)
                result = json.loads(msg)

                if result["status"] == "success":
                    messagebox.showinfo("Success", "Course deleted successfully.")

                    message = f"courses:{mail}"
                    msg = client.send_message(message)
                    updated_courses_data = json.loads(msg)

                    courses_window.destroy()
                    open_courses_window(root, updated_courses_data, mail, client)
                else:
                    messagebox.showerror("Error", result["message"])

        for course in teacher_courses:
            frame = tk.Frame(teacher_frame, bg="#d1f2eb")
            frame.pack(fill="x", pady=5)

            btn_course = tk.Button(frame, text=course['name'], font=("Arial", 16),
                                   width=20, command=lambda c=course: CourseWindow(root, c, is_teacher=True))
            btn_course.pack(side="left", padx=5, fill="x", expand=True)

            btn_delete = tk.Button(frame, text="❌", font=("Arial", 14), fg="red",
                                   command=lambda c=course: handle_delete_course(c))
            btn_delete.pack(side="right", padx=5)

    # ✅ Student Courses Section
    if student_courses:
        student_frame = tk.Frame(courses_window, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#f5b7b1")  # Light red
        student_frame.pack(pady=10, fill=tk.X, expand=True)

        tk.Label(student_frame, text="My Courses as Student", font=("Arial", 16, "bold"), bg="#f5b7b1").pack()

        for course in student_courses:
            frame = tk.Frame(student_frame, bg="#f5b7b1")
            frame.pack(fill="x", pady=5)

            btn_course = tk.Button(frame, text=course['name'], font=("Arial", 16),
                                   width=20, command=lambda c=course: CourseWindow(root, c, is_teacher=False))
            btn_course.pack(side="left", padx=5, fill="x", expand=True)

    # ✅ "Create New Course" button
    btn_create_new_course = tk.Button(courses_window, text="צור כיתה חדשה", font=("Arial", 16), width=20, height=2,
                                      command=lambda: create_new_course(mail, client, root))
    btn_create_new_course.pack(pady=10)

    # ✅ "Join Course" button
    btn_join_course = tk.Button(courses_window, text="הצטרף לכיתה", font=("Arial", 16), width=20, height=2,
                                command=lambda: join_course_window(mail, client, root))
    btn_join_course.pack(pady=10)

    courses_window.mainloop()

def create_new_course(mail, client, root):
    """Opens a window to create a new course."""
    new_course_window = tk.Toplevel()
    new_course_window.title("Create New Course")
    new_course_window.geometry("400x300")

    label_name = tk.Label(new_course_window, text="Course Name:", font=("Arial", 12))
    label_name.pack(pady=5)
    entry_name = tk.Entry(new_course_window, font=("Arial", 12))
    entry_name.pack(pady=5)

    label_subject = tk.Label(new_course_window, text="Subject:", font=("Arial", 12))
    label_subject.pack(pady=5)
    subject_options = ["Physics", "English", "Mathematics", "History"]
    combo_subject = tk.ttk.Combobox(new_course_window, values=subject_options, font=("Arial", 12))
    combo_subject.pack(pady=5)
    combo_subject.set(subject_options[0])

    def on_create_button_click():
        course_name = entry_name.get()
        subject = combo_subject.get()

        if not course_name:
            error_label.config(text="Course name cannot be empty.", fg="red")
            return

        new_course = {
            "name": course_name,
            "subject": subject,
            "teacher_mail": mail,
            "tasks": []
        }

        dump = json.dumps(new_course)
        message = f"new_course:{dump}"
        msg = client.send_message(message)
        result = json.loads(msg)

        if result["status"] == "success":
            messagebox.showinfo("Success", "Course added successfully.")
            new_course_window.destroy()

            message = f"courses:{mail}"
            msg = client.send_message(message)
            updated_courses_data = json.loads(msg)
            open_courses_window(root, updated_courses_data, mail, client)
        else:
            messagebox.showerror("Error", result["message"])

    create_button = tk.Button(new_course_window, text="Create", font=("Arial", 12), command=on_create_button_click)
    create_button.pack(pady=20)

    error_label = tk.Label(new_course_window, text="", font=("Arial", 10))
    error_label.pack(pady=5)

def join_course_window(mail, client, root):
    """Opens a popup for the user to enter a Course ID to join."""
    join_window = tk.Toplevel()
    join_window.title("הצטרף לכיתה")
    join_window.geometry("400x200")

    label_course_id = tk.Label(join_window, text="Enter Course ID:", font=("Arial", 12))
    label_course_id.pack(pady=5)
    entry_course_id = tk.Entry(join_window, font=("Arial", 12))
    entry_course_id.pack(pady=5)

    def on_join_button_click():
        course_id = entry_course_id.get().strip()

        if not course_id:
            messagebox.showerror("Error", "Course ID cannot be empty.")
            return

        join_course = {
            "course_id": course_id,
            "student_mail": mail
        }

        dump = json.dumps(join_course)
        message = f"join_course:{dump}"
        msg = client.send_message(message)
        result = json.loads(msg)

        if result["status"] == "success":
            messagebox.showinfo("Success", "Joined course successfully!")
            join_window.destroy()

            # Refresh courses window after joining
            message = f"courses:{mail}"
            msg = client.send_message(message)
            updated_courses_data = json.loads(msg)
            open_courses_window(root, updated_courses_data, mail, client)
        else:
            messagebox.showerror("Error", result["message"])

    join_button = tk.Button(join_window, text="Join", font=("Arial", 12), command=on_join_button_click)
    join_button.pack(pady=10)
import json
import tkinter as tk
from tkinter import messagebox
# from classroom_server.database import delete_course
from classroom_client.course_gui import CourseWindow
from main_client import Client

# client = Client()
# client.connect()
def open_courses_window(root, courses_data, mail, client):
    """Opens the courses window and displays courses where the user is a teacher or student."""
    global courses_window

    if 'courses_window' in globals() and courses_window:
        try:
            if courses_window.winfo_exists():
                courses_window.destroy()
        except:
            pass

    courses_window = tk.Toplevel(root)
    courses_window.title("בחר כיתה")
    courses_window.geometry("800x600")

    label_courses = tk.Label(courses_window, text="בחר כיתה", font=("Arial", 20))
    label_courses.pack(pady=10)

    teacher_courses = courses_data.get('teacher_courses', [])
    student_courses = courses_data.get('student_courses', [])

    # ✅ Teacher Courses Section
    if teacher_courses:
        teacher_frame = tk.Frame(courses_window, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#d1f2eb")  # Light green
        teacher_frame.pack(pady=10, fill=tk.X, expand=True)

        tk.Label(teacher_frame, text="My Courses as Teacher", font=("Arial", 16, "bold"), bg="#d1f2eb").pack()

        def handle_delete_course(course):
            confirm = messagebox.askyesno("Delete Course", f"Are you sure you want to delete {course['name']}?")
            if confirm:
                # result = delete_course(course["id"])
                course_id = course["_id"]
                message = f"delete_course:{course_id}"
                msg = client.send_message(message)
                result = json.loads(msg)

                if result["status"] == "success":
                    messagebox.showinfo("Success", "Course deleted successfully.")

                    message = f"courses:{mail}"
                    msg = client.send_message(message)
                    updated_courses_data = json.loads(msg)

                    courses_window.destroy()
                    open_courses_window(root, updated_courses_data, mail, client)
                else:
                    messagebox.showerror("Error", result["message"])

        for course in teacher_courses:
            frame = tk.Frame(teacher_frame, bg="#d1f2eb")
            frame.pack(fill="x", pady=5)

            btn_course = tk.Button(frame, text=course['name'], font=("Arial", 16),
                                   width=20, command=lambda c=course: CourseWindow(root, c,True,client))
            btn_course.pack(side="left", padx=5, fill="x", expand=True)

            btn_delete = tk.Button(frame, text="❌", font=("Arial", 14), fg="red",
                                   command=lambda c=course: handle_delete_course(c))
            btn_delete.pack(side="right", padx=5)

    # ✅ Student Courses Section
    if student_courses:
        student_frame = tk.Frame(courses_window, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#f5b7b1")  # Light red
        student_frame.pack(pady=10, fill=tk.X, expand=True)

        tk.Label(student_frame, text="My Courses as Student", font=("Arial", 16, "bold"), bg="#f5b7b1").pack()

        for course in student_courses:
            frame = tk.Frame(student_frame, bg="#f5b7b1")
            frame.pack(fill="x", pady=5)

            btn_course = tk.Button(frame, text=course['name'], font=("Arial", 16),
                                   width=20, command=lambda c=course: CourseWindow(root, c, is_teacher=False))
            btn_course.pack(side="left", padx=5, fill="x", expand=True)

    # ✅ "Create New Course" button
    btn_create_new_course = tk.Button(courses_window, text="צור כיתה חדשה", font=("Arial", 16), width=20, height=2,
                                      command=lambda: create_new_course(mail, client, root))
    btn_create_new_course.pack(pady=10)

    # ✅ "Join Course" button
    btn_join_course = tk.Button(courses_window, text="הצטרף לכיתה", font=("Arial", 16), width=20, height=2,
                                command=lambda: join_course_window(mail, client, root))
    btn_join_course.pack(pady=10)

    courses_window.mainloop()

def create_new_course(mail, client, root):
    """Opens a window to create a new course."""
    new_course_window = tk.Toplevel()
    new_course_window.title("Create New Course")
    new_course_window.geometry("400x300")

    label_name = tk.Label(new_course_window, text="Course Name:", font=("Arial", 12))
    label_name.pack(pady=5)
    entry_name = tk.Entry(new_course_window, font=("Arial", 12))
    entry_name.pack(pady=5)

    label_subject = tk.Label(new_course_window, text="Subject:", font=("Arial", 12))
    label_subject.pack(pady=5)
    subject_options = ["Physics", "English", "Mathematics", "History"]
    combo_subject = tk.ttk.Combobox(new_course_window, values=subject_options, font=("Arial", 12))
    combo_subject.pack(pady=5)
    combo_subject.set(subject_options[0])

    def on_create_button_click():
        course_name = entry_name.get()
        subject = combo_subject.get()

        if not course_name:
            error_label.config(text="Course name cannot be empty.", fg="red")
            return

        new_course = {
            "name": course_name,
            "subject": subject,
            "teacher_mail": mail,
            "tasks": []
        }

        dump = json.dumps(new_course)
        message = f"new_course:{dump}"
        msg = client.send_message(message)
        result = json.loads(msg)

        if result["status"] == "success":
            messagebox.showinfo("Success", "Course added successfully.")
            new_course_window.destroy()

            message = f"courses:{mail}"
            msg = client.send_message(message)
            updated_courses_data = json.loads(msg)
            open_courses_window(root, updated_courses_data, mail, client)
        else:
            messagebox.showerror("Error", result["message"])

    create_button = tk.Button(new_course_window, text="Create", font=("Arial", 12), command=on_create_button_click)
    create_button.pack(pady=20)

    error_label = tk.Label(new_course_window, text="", font=("Arial", 10))
    error_label.pack(pady=5)

def join_course_window(mail, client, root):
    """Opens a popup for the user to enter a Course ID to join."""
    join_window = tk.Toplevel()
    join_window.title("הצטרף לכיתה")
    join_window.geometry("400x200")

    label_course_id = tk.Label(join_window, text="Enter Course ID:", font=("Arial", 12))
    label_course_id.pack(pady=5)
    entry_course_id = tk.Entry(join_window, font=("Arial", 12))
    entry_course_id.pack(pady=5)

    def on_join_button_click():
        course_id = entry_course_id.get().strip()

        if not course_id:
            messagebox.showerror("Error", "Course ID cannot be empty.")
            return

        join_course = {
            "course_id": course_id,
            "student_mail": mail
        }

        dump = json.dumps(join_course)
        message = f"join_course:{dump}"
        msg = client.send_message(message)
        result = json.loads(msg)

        if result["status"] == "success":
            messagebox.showinfo("Success", "Joined course successfully!")
            join_window.destroy()

            # Refresh courses window after joining
            message = f"courses:{mail}"
            msg = client.send_message(message)
            updated_courses_data = json.loads(msg)
            open_courses_window(root, updated_courses_data, mail, client)
        else:
            messagebox.showerror("Error", result["message"])

    join_button = tk.Button(join_window, text="Join", font=("Arial", 12), command=on_join_button_click)
    join_button.pack(pady=10)
