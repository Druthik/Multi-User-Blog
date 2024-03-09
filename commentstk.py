import tkinter as tk
import tkinter.messagebox as messagebox
import db_configtk
import mysql.connector
import customtkinter as ctk
from tkinter import *

# Function to fetch comments for a specific post
def fetch_comments(post_id):
    conn = mysql.connector.connect(**db_configtk.db_config)

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
        comments = cursor.fetchall()
        return comments
    
    except mysql.connector.Error as e:
        print("Error fetching comments:", e)
        return []
    
    finally:
        cursor.close()
        conn.close()

# Function to display comments for a specific post
def display_comments(post_id, username):
    comments = fetch_comments(post_id)
    comment_window = tk.Tk()
    window_width = comment_window.winfo_screenwidth() // 2
    window_height = comment_window.winfo_screenheight() // 2
    comment_window.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
    comment_window.title("Comments")
    frame = Frame(master=comment_window, borderwidth=5, height=50, relief="groove")
    frame.pack(pady=20, padx=40, fill="both" , expand=True)

    scrollbar = ctk.CTkScrollableFrame(master=frame, orientation='vertical')
    scrollbar.pack(fill='both', expand=True)
    # Display each comment
    if len(comments)==0:
        print("No comments")
        comment_text_label = ctk.CTkLabel(master=scrollbar, text="No comments yet, be the first to comment", font=("Calibri Body", 16, "bold"), wraplength=400, justify="left")
        comment_text_label.pack(padx=0, pady=5, anchor="w")

        #add_comment_button = tk.Button(master=frame, text="Add Comment", font=("Calibri Body", 14, "bold"), command=lambda: Add_Comment())
        #add_comment_button.pack(pady=5)

        comment_text_entry = Text(master=frame, width=50, height=5, font=("Calibri Body", 14, "bold"))
        comment_text_entry.pack(pady=10)

        def submit_comment():
            comment_text = comment_text_entry.get("1.0", tk.END).strip()

            if not comment_text:
                messagebox.showerror("Error", "Please enter comment.")
                return
            
            # Implement the add_comment function to add the comment to the database
            # Remember to handle potential errors and provide appropriate feedback
            comment_added_successfully = add_comment(post_id, username, comment_text)
            if comment_added_successfully:
                #parent_window.deiconify()  # Show the comment window again
                comment_window.destroy()  # Close the add comment window
                display_comments(post_id, username)
            else:
                messagebox.showerror("Error", "Failed to add comment. Please try again.")

        # Submit button
        submit_button = tk.Button(master=frame, text="Add Comment", font=("Calibri Body", 14, "bold"), command=submit_comment)
        submit_button.pack()
    else:
        for comment in comments:
            cmnt = comment[2]+" :  "+comment[3]
            #print(cmnt)
            comment_text_label = ctk.CTkLabel(master=scrollbar, text=cmnt, font=("Calibri Body", 16, "bold"), wraplength=400, justify="left")
            comment_text_label.pack(padx=0, pady=5, anchor="w")

        #add_comment_button = tk.Button(master=frame, text="Add Comment", font=("Calibri Body", 14, "bold"), command=lambda: Add_Comment())
        #add_comment_button.pack(pady=5)

        comment_text_entry = Text(master=frame, width=50, height=5, font=("Calibri Body", 14, "bold"))
        comment_text_entry.pack(pady=10)

        def submit_comment():
            comment_text = comment_text_entry.get("1.0", tk.END).strip()

            if not comment_text:
                messagebox.showerror("Error", "Please enter comment.")
                return

            # Implement the add_comment function to add the comment to the database
            # Remember to handle potential errors and provide appropriate feedback
            comment_added_successfully = add_comment(post_id, username, comment_text)
            if comment_added_successfully:
                #parent_window.deiconify()  # Show the comment window again
                comment_window.destroy()  # Close the add comment window
                display_comments(post_id, username)
            else:
                messagebox.showerror("Error", "Failed to add comment. Please try again.")

        # Submit button
        submit_button = tk.Button(master=frame, text="Add Comment", font=("Calibri Body", 14, "bold"), command=submit_comment)
        submit_button.pack()

    comment_text_label.mainloop()

# Function to add a new comment to a post
def add_comment(post_id, username, comment_text):
    # Connect to the database
    conn = mysql.connector.connect(**db_configtk.db_config)

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (post_id, username, comment_text) VALUES (%s, %s, %s)",
                       (post_id, username, comment_text))
        conn.commit()

        messagebox.showinfo("Success", "Comment added successfully!")
        return True
    except mysql.connector.Error as e:
        print("Error adding comment:", e)
        messagebox.showerror("Error", "Failed to add comment.")
    finally:
        cursor.close()
        conn.close()

