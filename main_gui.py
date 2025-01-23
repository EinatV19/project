import tkinter as tk
from tkinter import messagebox

# רשימת כיתות לדוגמה
courses = ["מתמטיקה", "מדעי המחשב", "ספרות", "אזרחות", "פיזיקה", "ביולוגיה", "אנגלית", "היסטוריה"]


# פונקציה להדפסת הודעת הצלחה לאחר התחברות
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "teacher" and password == "1234":  # בדיקת שם משתמש וסיסמה לדוגמה
        open_courses_window()
    else:
        messagebox.showerror("Error", "שם משתמש או סיסמה שגויים!")

# פתיחת חלון כיתות לאחר התחברות
def open_courses_window():
    login_window.destroy()  # סגירת חלון ההתחברות
    courses_window = tk.Tk()
    courses_window.title("בחר כיתה")

    # כותרת
    label_courses = tk.Label(courses_window, text="בחר כיתה", font=("Arial", 20))
    label_courses.pack(pady=20)

    # כפתורים עבור כל כיתה
    for course in courses:
        btn_course = tk.Button(courses_window, text=course, font=("Arial", 16), width=20, height=2,
                               command=lambda c=course: open_class_window(c))
        btn_course.pack(pady=10)

    courses_window.mainloop()


# חלון עבור כיתה נבחרת
def open_class_window(course):
    class_window = tk.Tk()
    class_window.title(f"כיתה - {course}")

    # כותרת של הכיתה
    label_class = tk.Label(class_window, text=f"ברוך הבא לכיתה {course}!", font=("Arial", 20))
    label_class.pack(pady=20)

    # כפתורים לפונקציות בכיתה
    btn_class_chat = tk.Button(class_window, text="צ'אט כיתתי", font=("Arial", 16), width=20, height=2,
                               command=open_class_chat)
    btn_class_chat.pack(pady=10)

    btn_private_chat = tk.Button(class_window, text="צ'אט פרטי", font=("Arial", 16), width=20, height=2,
                                 command=open_private_chat)
    btn_private_chat.pack(pady=10)

    btn_video_conference = tk.Button(class_window, text="שיחת ועידה", font=("Arial", 16), width=20, height=2,
                                     command=open_video_conference)
    btn_video_conference.pack(pady=10)

    btn_assignments = tk.Button(class_window, text="משימות", font=("Arial", 16), width=20, height=2,
                                command=open_assignments)
    btn_assignments.pack(pady=10)

    class_window.mainloop()


# פונקציות למודולים בכיתה
def open_class_chat():
    messagebox.showinfo("צ'אט כיתתי", "כאן תוכל לשלוח הודעות לכל תלמידי הכיתה.")


def open_private_chat():
    messagebox.showinfo("צ'אט פרטי", "כאן תוכל לשלוח הודעות אישיות לתלמידים.")


def open_video_conference():
    messagebox.showinfo("שיחת ועידה", "כאן תוכל להצטרף לשיחת ועידה עם המורה והכיתה.")


def open_assignments():
    messagebox.showinfo("משימות", "כאן תוכל להעלות קבצים עבור המשימות שלך.")


# יצירת חלון התחברות
login_window = tk.Tk()
login_window.title("התחברות למערכת")

# שדות התחברות
label_username = tk.Label(login_window, text="שם משתמש:", font=("Arial", 14))
label_username.pack(pady=10)

entry_username = tk.Entry(login_window, font=("Arial", 14))
entry_username.pack(pady=10)

label_password = tk.Label(login_window, text="סיסמה:", font=("Arial", 14))
label_password.pack(pady=10)

entry_password = tk.Entry(login_window, font=("Arial", 14), show="*")
entry_password.pack(pady=10)

btn_login = tk.Button(login_window, text="התחבר", font=("Arial", 16), width=20, height=2, command=login)
btn_login.pack(pady=20)

login_window.mainloop()

