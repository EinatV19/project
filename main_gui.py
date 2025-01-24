import json
import tkinter as tk
from tkinter import messagebox

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
        result = client.send_message(message)
        result = json.loads(result)

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
    result = client.send_message(message)
    result = json.loads(result)

    if result['status'] == 'success':  # בדיקת שם משתמש וסיסמה לדוגמה
        open_courses_window()
    else:
        messagebox.showerror("Error", message)

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
