import tkinter as tk
import mysql.connector
import tkinter.messagebox as tkmb
import db_configtk
import subprocess

def get_user_information(username):
    # Connect to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_configtk.db_config)
    cursor = conn.cursor()

    # Execute a query to fetch user information based on the username
    cursor.execute("SELECT email, phone FROM users WHERE username=%s", (username,))
    user_info = cursor.fetchone()  # Assuming only one row for each username

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return user_info

def update_user_information(username, email, phone):
    # Connect to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_configtk.db_config)
    cursor = conn.cursor()

    # Execute a query to update user information based on the username
    cursor.execute("UPDATE users SET email=%s, phone=%s WHERE username=%s", (email, phone, username))

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def profile_page(username):
    def edit_email():
        email_entry.config(state="normal")
        email_edit_button.config(state="disabled")

    def edit_phone():
        phone_entry.config(state="normal")
        phone_edit_button.config(state="disabled")

    def save_changes():
        new_email = email_entry.get()
        new_phone = phone_entry.get()

        update_user_information(username, new_email, new_phone)

        email_entry.config(state="disabled")
        phone_entry.config(state="disabled")
        email_edit_button.config(state="normal")
        phone_edit_button.config(state="normal")

    def delete_post(post_id):
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
        load_posts()

    def edit_post(post_id, post_content_entry):
        new_content = post_content_entry.get()
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET text_data=%s WHERE id=%s", (new_content, post_id))
        conn.commit()
        cursor.close()
        conn.close()
        load_posts()

    def load_posts():
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, heading FROM posts WHERE username=%s", (username,))
        posts = cursor.fetchall()
        cursor.close()
        conn.close()

        for post_frame in post_frames:
            post_frame.destroy()

        post_frames.clear()

        for post_id, heading in posts:
            post_frame = tk.Frame(profile_window)
            post_frame.pack(pady=10)

            post_content_entry = tk.Entry(post_frame, font=("Ink Free", 12))
            post_content_entry.insert(0, heading)
            post_content_entry.pack(side="left", padx=10)

            edit_button = tk.Button(post_frame, text="Edit", font=("Ink Free", 12, "bold"), command=lambda post_id=post_id, entry=post_content_entry: edit_post(post_id, entry))
            edit_button.pack(side="left", padx=10)

            delete_button = tk.Button(post_frame, text="Delete", font=("Ink Free", 12, "bold"), command=lambda post_id=post_id: delete_post(post_id))
            delete_button.pack(side="left", padx=10)

            post_frames.append(post_frame)

    def go_back():
        profile_window.destroy()
        subprocess.run(["python", "homepagetk.py"])

    # Create a new window for the profile page
    profile_window = tk.Tk()
    profile_window.attributes('-fullscreen', True)
    profile_window.title("My Profile")

    label = tk.Label(profile_window, text="Daily Post", font=("Ink Free", 50, "bold"))
    label.pack(pady=50)

    # Fetch user information from the database
    email, phone = get_user_information(username)

    # Display user information
    username_label = tk.Label(profile_window, text=f"Welcome, {username}!", font=("Ink Free", 20, "bold"))
    username_label.pack(pady=20)

    email_frame = tk.Frame(profile_window)
    email_frame.pack(pady=10)

    email_entry = tk.Entry(email_frame, font=("Ink Free", 14, "bold"), width=30)
    email_entry.insert(0, email)
    email_entry.config(state="disabled")
    email_entry.pack(side="left", padx=10)

    email_edit_button = tk.Button(email_frame, text="✎", command=edit_email)
    email_edit_button.pack(side="left")

    phone_frame = tk.Frame(profile_window)
    phone_frame.pack(pady=10)

    phone_entry = tk.Entry(phone_frame, font=("Ink Free", 14, "bold"), width=30)
    phone_entry.insert(0, phone)
    phone_entry.config(state="disabled")
    phone_entry.pack(side="left", padx=10)

    phone_edit_button = tk.Button(phone_frame, text="✎", command=edit_phone)
    phone_edit_button.pack(side="left")

    save_button = tk.Button(profile_window, text="Save Changes", font=("Ink Free", 12, "bold"), command=save_changes)
    save_button.pack(pady=10)

    post_frames = []

    # Load and display user's posts
    load_posts()

    back_button = tk.Button(profile_window, text="Go Back", font=("Ink Free", 12, "bold"), command=go_back)
    back_button.pack(pady=10)

    # Run the tkinter event loop
    profile_window.mainloop()
