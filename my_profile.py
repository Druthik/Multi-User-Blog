import customtkinter as ctk  # Import CustomTkinter
import tkinter as tk  # Import tkinter for additional widgets

def profile_page(username):
    # Create a new window for the profile page
    profile_window = ctk.CTkToplevel()
    profile_window.attributes('-fullscreen', True)
    #profile_window.geometry("500x400")  # Set initial window size
    profile_window.title("My Profile")

    # Design your profile page content here
    # Add widgets like labels, entries, images, etc. to display user information

    # Example: Display a welcome message with the username
    username_label = ctk.CTkLabel(profile_window, text=f"Welcome, {username}!", font=("Ink Free", 20, "bold"))
    username_label.pack(pady=20)

    # ... (Add more widgets and design elements as needed)
