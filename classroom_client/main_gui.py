import tkinter as tk
from auth_gui import login, open_register_window
from main_client import Client

# Create a single instance of Client (Only 1 connection to the server)
client = Client()
client.connect()

# Create login window
login_window = tk.Tk()
login_window.title("התחברות למערכת")
login_window.geometry("400x600")

label_username = tk.Label(login_window, text="שם משתמש:", font=("Arial", 14))
label_username.pack(pady=10)

entry_mail = tk.Entry(login_window, font=("Arial", 14))
entry_mail.pack(pady=10)

label_password = tk.Label(login_window, text="סיסמה:", font=("Arial", 14))
label_password.pack(pady=10)

entry_password = tk.Entry(login_window, font=("Arial", 14), show="*")
entry_password.pack(pady=10)

btn_login = tk.Button(login_window, text="התחבר", font=("Arial", 16), width=20, height=2,
                      command=lambda: login(entry_mail, entry_password, login_window, client))
btn_login.pack(pady=20)

btn_register = tk.Button(login_window, text="הרשמה", font=("Arial", 16), width=20, height=2,
                         command=lambda : open_register_window(client))
btn_register.pack(pady=10)

login_window.mainloop()
