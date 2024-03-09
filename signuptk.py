import tkinter as tk
from functionstk import signup

signup_app = tk.Tk()
signup_app.attributes('-fullscreen', True)  # Make the application fullscreen
signup_app.title("Signup - Daily Post")

# Adjusted label with bigger text and changed font
label = tk.Label(signup_app, text="Daily Post", font=("Ink Free", 100, "bold"))
label.pack(pady=50)

frame = tk.Frame(master=signup_app, borderwidth=2)
frame.pack(pady=20, padx=40)

signup_user_placeholder = tk.Label(master=frame, text='Enter Username', font=("Ink Free", 16, "bold"))
signup_user_placeholder.grid(row=0, column=0, sticky="w", pady=(0,5))

signup_user_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
signup_user_entry.grid(row=1, column=0, pady=5)

signup_pass_placeholder = tk.Label(master=frame, text='Enter Password', font=("Ink Free", 16, "bold"))
signup_pass_placeholder.grid(row=2, column=0, sticky="w", pady=(10,5))

signup_user_pass = tk.Entry(master=frame, show="*", width=30, font=("Ink Free", 16, "bold"))
signup_user_pass.grid(row=3, column=0, pady=5)

signup_email_placeholder = tk.Label(master=frame, text='Enter Email', font=("Ink Free", 16, "bold"))
signup_email_placeholder.grid(row=4, column=0, sticky="w", pady=(10,5))

signup_email_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
signup_email_entry.grid(row=5, column=0, pady=5)

signup_phone_placeholder = tk.Label(master=frame, text='Enter Phone Number', font=("Ink Free", 16, "bold"))
signup_phone_placeholder.grid(row=6, column=0, sticky="w", pady=(10,5))

signup_phone_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
signup_phone_entry.grid(row=7, column=0, pady=5)

def create_account():
    result = signup(signup_user_entry, signup_user_pass, signup_email_entry, signup_phone_entry)
    print(result)
    if result:  # Assuming signup function returns True on success
        signup_app.destroy()  # Close the signup window

signup_button = tk.Button(master=frame, text="Create Account", font=("Ink Free", 16, "bold"), command=create_account)
signup_button.grid(row=8, column=0, pady=20)

signup_app.mainloop()
