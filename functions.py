# functions.py
import mysql.connector
import tkinter.messagebox as tkmb
import customtkinter as ctk
import db_config

def login(user_entry, user_pass):
    # Connect to the MySQL database
    try:
        connection = mysql.connector.connect(**db_config.db_config)
        cursor = connection.cursor()
    
        # Perform a SELECT query to check the username and password
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (user_entry.get(), user_pass.get()))
        result = cursor.fetchone()

        if result:
            print(user_entry.get()+" login"+" successful.")
            op=True
            #tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
            #ctk.CTkLabel(ctk.login_app, text="Daily Post to learn new!!", font=("Ink Free", 45)).pack()
            return op
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username or password")

    except mysql.connector.Error as err:
        tkmb.showerror(title="Database Error", message=f"Error: {err}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def signup(signup_user_entry, signup_user_pass, signup_email_entry, signup_phone_entry):
    #signup_window = ctk.CTk()
    #signup_window = ctk.CTkToplevel(ctk.app)
    #signup_window.title("Signup")
    try:
        db = mysql.connector.connect(**db_config.db_config)
        cursor = db.cursor()
        # Check if the username already exists
        check_query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(check_query, (signup_user_entry.get(),))
        existing_user = cursor.fetchone()

        if existing_user:
            tkmb.showwarning(title="Signup Failed", message="Username already exists. Please choose a different username.")
        else:
            # Insert into blog_author
            cursor.execute('INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)',
                        (signup_user_entry.get(),
                         signup_user_pass.get(),
                         signup_email_entry.get(),
                         signup_phone_entry.get()))
            db.commit()
            tkmb.showinfo(title="Signup Successful", message="Account created successfully. You can now log in.")
            return True
            #signup_window.destroy()  # Close the signup window after successful signup
            
    except Exception as e:
        print('Error in signing up:', e)
        db.rollback()
        msg = 'Operation Failed'

    finally:
        # Close the database connection
        if db.is_connected():
            cursor.close()
            db.close()

