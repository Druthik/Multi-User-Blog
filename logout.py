# logout.py

import customtkinter as ctk

# Function to handle the logout action
def logout(hpage, logout_window):
    hpage.destroy()  # Destroy the main page
    logout_window.destroy()  # Destroy the logout window

# Create a new window for the logout page
def logout_page(hpage):

    # Selecting GUI theme - dark, light, system (for system default)
    ctk.set_appearance_mode("light")
    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("blue")
    logout_window = ctk.CTk()
    logout_window.attributes('-fullscreen', False)  # Set the window to fullscreen
    logout_window.title("Logout")

    # Add a label to display a logout confirmation message
    logout_label = ctk.CTkLabel(logout_window, text="Are you sure you want to logout?", font=("Ink Free", 18, "bold"))
    logout_label.pack()

    # Add a button to confirm the logout action
    confirm_button = ctk.CTkButton(logout_window, text="Logout", font=("Ink Free", 18), command=lambda: logout(hpage, logout_window))
    confirm_button.pack(pady=10)

    # Run the logout window's main loop
    logout_window.mainloop()

    return logout_window  # Return the logout window object
