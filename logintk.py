import tkinter as tk
import subprocess
from functionstk import login
import os
from forgotpasstk import open_password_reset_window  

login_app = tk.Tk()
login_app.attributes('-fullscreen', True)  # Make the application fullscreen
login_app.title("Daily Post Login")

# Adjusted label with bigger text and changed font
label = tk.Label(login_app, text="Daily Post", font=("Ink Free", 100, "bold"))
label.pack(pady=50)

frame = tk.Frame(master=login_app, borderwidth=2)
frame.pack(pady=20, padx=40)

label_username = tk.Label(master=frame, text='Username', font=("Ink Free", 16, "bold"))
label_username.grid(row=0, column=0, sticky="w", pady=(0,5))

user_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
user_entry.grid(row=1, column=0, pady=5)

label_password = tk.Label(master=frame, text='Password', font=("Ink Free", 16, "bold"))
label_password.grid(row=2, column=0, sticky="w", pady=(10,5))

user_pass = tk.Entry(master=frame, show="*", width=30, font=("Ink Free", 16, "bold"))
user_pass.grid(row=3, column=0, pady=5)

forgotpass = tk.Label(master=frame, text="Forgot password?", cursor='hand2', font=("Ink Free", 16, "bold"), justify='left')
forgotpass.bind("<Button-1>", lambda event: open_password_reset_window(login_app)) 
forgotpass.grid(row=4, column=0, sticky="w", pady=(15,5))

def login_success():
    op = login(user_entry, user_pass)
    username_str = user_entry.get()
    os.environ["USERNAME"] = username_str
    if op:
        login_app.destroy()
        subprocess.run(["python", "homepagetk.py"])

button_login = tk.Button(master=frame, text='Login', font=("Ink Free", 16, "bold"), command=login_success)
button_login.grid(row=5, column=0, pady=15)

frame1 = tk.Frame(master=login_app, borderwidth=2)
frame1.pack(pady=20, padx=40)

signup_label = tk.Label(master=frame1, text="Don't have an account?", font=("Ink Free", 15, "bold"))
signup_label.grid(row=0, column=0, sticky="w", pady=5)

def open_signup():
    subprocess.run(["python", "signuptk.py"])  # Execute signup.py using subprocess

button_signup = tk.Button(master=frame1, text='Signup', font=("Ink Free", 16, "bold"), command=open_signup)
button_signup.grid(row=1, column=0, pady=10)

login_app.mainloop()
