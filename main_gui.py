import json
import tkinter as tk
from tkinter import messagebox, ttk

from course_gui2 import CourseWindow
from db.db_utils import check_user
from main_client import Client

# רשימת כיתות לדוגמה
courses = ["מתמטיקה", "מדעי המחשב", "ספרות", "אזרחות", "פיזיקה", "ביולוגיה", "אנגלית", "היסטוריה"]

client = Client()

# Connect to the server
client.connect()

# פונקציה לפתיחת חלון רישום
def open_register_window():
    register_window = tk.Tk()
    register_window.title("הרשמה למערכת")

    # שדות הרשמה
    label_mail = tk.Label(register_window, text="דוא\"ל:", font=("Arial", 14))  # החלפתי את הגרשיים
    label_mail.pack(pady=10)
    entry_register_mail = tk.Entry(register_window, font=("Arial", 14))
    entry_register_mail.pack(pady=10)

    label_register_password = tk.Label(register_window, text="סיסמה:", font=("Arial", 14))
    label_register_password.pack(pady=10)
    entry_register_password = tk.Entry(register_window, font=("Arial", 14), show="*")
    entry_register_password.pack(pady=10)

    def register_user():
        mail = entry_register_mail.get()
        password = entry_register_password.get()

        message = f"register:{mail},{password}"
        msg = client.send_message(message)
        result = json.loads(msg)

        if result['status'] == 'success':
            messagebox.showinfo("הרשמה", "ההרשמה בוצעה בהצלחה!")
            register_window.destroy()
        else:
            messagebox.showerror("שגיאה", "לא ניתן להרשם. בדוק את הנתונים ונסה שוב.")

    btn_register = tk.Button(register_window, text="הרשמה", font=("Arial", 16), width=20, height=2, command=register_user)
    btn_register.pack(pady=20)

    register_window.mainloop()

# פונקציה להדפסת הודעת הצלחה לאחר התחברות
def login():
    mail = entry_mail.get()
    password = entry_password.get()

    message = f"login:{mail},{password}"
    msg = client.send_message(message)
    result = json.loads(msg)

    if result['status'] == 'success':  # בדיקת שם משתמש וסיסמה לדוגמה
        message = f"courses:{mail}"
        msg = client.send_message(message)
        result = json.loads(msg)
        open_courses_window(result)
    else:
        messagebox.showerror("Error", message)

# פתיחת חלון כיתות לאחר התחברות
def open_courses_window(courses_data):
    # Close the login window
    login_window.destroy()  # Close the login window (this assumes the login window is named login_window)

    # Create a new window for courses
    courses_window = tk.Tk()
    courses_window.title("בחר כיתה")

    # Set the window size (optional, you can customize as needed)
    courses_window.geometry("600x400")

    # Add a label for the courses window
    label_courses = tk.Label(courses_window, text="בחר כיתה", font=("Arial", 20))
    label_courses.pack(pady=20)

    # Retrieve courses from the dictionary
    courses = courses_data.get('courses', [])

    # Create a button for each course in the dictionary
    for course in courses:
        course_name = course.get('name', 'Unknown Course')  # Use 'Unknown Course' if name is missing
        btn_course = tk.Button(courses_window, text=course_name, font=("Arial", 16), width=20, height=2,
                               command=lambda c=course: CourseWindow(None, c))  # Create a new window for the course
        btn_course.pack(pady=10)

    # Add a "Create New Course" button to open a new course creation window
    def create_new_course():
        # Create a new window for creating a new course
        new_course_window = tk.Toplevel()
        new_course_window.title("Create New Course")
        new_course_window.geometry("400x300")  # Set the window size

        # Add a label for the course name
        label_name = tk.Label(new_course_window, text="Course Name:", font=("Arial", 12))
        label_name.pack(pady=5)
        entry_name = tk.Entry(new_course_window, font=("Arial", 12))
        entry_name.pack(pady=5)

        # Add a label for the subject
        label_subject = tk.Label(new_course_window, text="Subject:", font=("Arial", 12))
        label_subject.pack(pady=5)
        subject_options = ["Physics", "English", "Mathematics", "History"]  # Add more subjects as needed
        combo_subject = ttk.Combobox(new_course_window, values=subject_options, font=("Arial", 12))
        combo_subject.pack(pady=5)
        combo_subject.set(subject_options[0])  # Set default subject

        # Function to handle the creation of a new course
        def on_create_button_click():
            course_name = entry_name.get()
            subject = combo_subject.get()

            if not course_name:
                # Display an error message if the course name is empty
                error_label.config(text="Course name cannot be empty.", fg="red")
                return


            # Create a new course document
            new_course = {
                "name": course_name,
                "subject": subject,
                "teacher_mail": "q"
            }


            # Close the new course window
            new_course_window.destroy()

            # Optionally, update the courses list in the main window
            # update_courses_list()
            # Add a button to create the new course

        create_button = tk.Button(new_course_window, text="Create", font=("Arial", 12), command=on_create_button_click)
        create_button.pack(pady=20)

        # Label to display error messages
        error_label = tk.Label(new_course_window, text="", font=("Arial", 10))
        error_label.pack(pady=5)

        # Run the new course window event loop
        new_course_window.mainloop()
    btn_create_new_course = tk.Button(courses_window, text="Create New Course", font=("Arial", 16), width=20, height=2,
                                      command=create_new_course)
    btn_create_new_course.pack(pady=10)

    # Run the courses window event loop
    courses_window.mainloop()


# יצירת חלון התחברות
login_window = tk.Tk()
login_window.title("התחברות למערכת")

# שדות התחברות
label_username = tk.Label(login_window, text="שם משתמש:", font=("Arial", 14))
label_username.pack(pady=10)

entry_mail = tk.Entry(login_window, font=("Arial", 14))
entry_mail.pack(pady=10)

label_password = tk.Label(login_window, text="סיסמה:", font=("Arial", 14))
label_password.pack(pady=10)

entry_password = tk.Entry(login_window, font=("Arial", 14), show="*")
entry_password.pack(pady=10)

btn_login = tk.Button(login_window, text="התחבר", font=("Arial", 16), width=20, height=2, command=login)
btn_login.pack(pady=20)

# כפתור להרשמה
btn_register = tk.Button(login_window, text="הרשמה", font=("Arial", 16), width=20, height=2, command=open_register_window)
btn_register.pack(pady=10)

login_window.mainloop()
