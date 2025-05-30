import json
import tkinter as tk
from tkinter import messagebox
from course_manager import open_courses_window  # ✅ Fixed import

def open_register_window(client):  # ✅ Accept `client` as an argument
    """Opens the registration window."""
    register_window = tk.Toplevel()
    register_window.title("הרשמה למערכת")
    register_window.geometry("400x300")

    label_mail = tk.Label(register_window, text="דוא\"ל:", font=("Arial", 14))
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
        msg = client.send_message(message)  # ✅ Now using the passed `client`
        result = json.loads(msg)

        if result['status'] == 'success':
            messagebox.showinfo("הרשמה", "ההרשמה בוצעה בהצלחה!")
            register_window.destroy()
        else:
            messagebox.showerror("שגיאה", "לא ניתן להרשם. בדוק את הנתונים ונסה שוב.")

    btn_register = tk.Button(register_window, text="הרשמה", font=("Arial", 16), width=20, height=2,
                             command=register_user)
    btn_register.pack(pady=20)

def login(entry_mail, entry_password, login_window, client):
    """Handles user login."""
    mail = entry_mail.get()
    password = entry_password.get()

    message = f"login:{mail},{password}"
    msg = client.send_message(message)
    result = json.loads(msg)

    if result['status'] == 'success':
        message = f"courses:{mail}"
        msg = client.send_message(message)
        courses_data = json.loads(msg)

        login_window.withdraw()
        open_courses_window(login_window, courses_data, mail, client)  # ✅ Pass `login_window` as root
    else:
        messagebox.showerror("Error", "Invalid login credentials.")
