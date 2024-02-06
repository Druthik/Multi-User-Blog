# ui.py
import customtkinter as ctk
import subprocess
from functions import login
import time
import os 

# Selecting GUI theme - dark, light, system (for system default)
ctk.set_appearance_mode("light")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")

login_app = ctk.CTk()
login_app.attributes('-fullscreen', True)  # Make the application fullscreen
login_app.title("Daily Post Login")

# Adjusted label with bigger text and changed font
label = ctk.CTkLabel(login_app, text="Daily Post", font=("Ink Free", 100, "bold"), corner_radius=20)
label.pack(pady=100)

frame = ctk.CTkFrame(master=login_app, border_width=2, corner_radius=20, height=50)
frame.pack(pady=20, padx=40, fill=None, expand=False)

label = ctk.CTkLabel(master=frame, text='Login', font=("Ink Free", 25, "bold"), corner_radius=10)
label.pack(pady=15, padx=100)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=200, font=("Ink Free", 16, "bold"))
user_entry.pack(side="top", anchor="center", pady=5, padx=25)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", width=200, font=("Ink Free", 16, "bold"))
user_pass.pack(side="top", anchor="center", pady=5, padx=25)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me', font=("Ink Free", 15), height=20, width=20)
checkbox.pack(side="top", anchor="center", pady=10, padx=25)

def login_success():
    op = login(user_entry, user_pass)
    username_str = user_entry.get()
    os.environ["USERNAME"] = username_str
    if op:
        login_app.destroy()
        subprocess.run(["python", "homepage.py"]) 
         
button_login = ctk.CTkButton(master=frame, text='Login', font=("Ink Free", 16, "bold"), command=login_success)
button_login.pack(side="top", anchor="center", pady=15, padx=100)

frame1 = ctk.CTkFrame(master=login_app, border_width=2, corner_radius=20, height=50)
frame1.pack(pady=20, padx=40, fill=None, expand=False)

signup_label = ctk.CTkLabel(master=frame1, text="Don't have an account?", font=("Ink Free", 15, "bold"))
signup_label.pack(pady=5)

def open_signup():
    subprocess.run(["python", "signup.py"])  # Execute signup.py using subprocess

button_signup = ctk.CTkButton(master=frame1, text='Signup', font=("Ink Free", 16, "bold"), command=open_signup)
button_signup.pack(side="top", anchor="center", pady=10, padx=100)

login_app.mainloop()
