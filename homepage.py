import customtkinter as ctk
from tkinter import *
import mysql.connector
import db_config
from PIL import Image, ImageTk, ImageDraw, ImageFont
from customtkinter import CTkImage 
from tkinter import filedialog
import os
import tkinter.ttk as ttk 
import logout
import my_profile

username = os.environ.get("USERNAME")  # Retrieve environment variable
print("Welcome "+ username)
hpage = None

def insert_post(image_path, text_data, user_name=username):
    try:
        connection = mysql.connector.connect(**db_config.db_config)
        cursor = connection.cursor()

        # Assuming your "posts" table has columns: id, image_path, text_data, username
        insert_query = "INSERT INTO posts (image_path, text_data, username) VALUES (%s, %s, %s)"
        post_data = (image_path, text_data, user_name)

        cursor.execute(insert_query, post_data)
        connection.commit()

        print("Post added successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to create a circular profile picture with the first letter of the username
def create_profile_picture(user_name, size):
    # Create a blank image with an alpha channel (RGBA)
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Set the font and size
    font_size = int(size[0] * 0.6)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Get the first letter of the username
    first_letter = user_name[0].upper()

    # Calculate the position to center the text
    text_width = draw.textlength(first_letter)
    x = (size[0] - text_width) // 2
    y = (size[1] - text_width) // 2

    # Draw the text on the image
    draw.text((x, y), first_letter, font=font, fill=(255, 255, 255, 255))

    return image

# Function for making round corners
def round_corners(image_path, corner_radius, output_size):
    # Load image using PhotoImage
    original_image = Image.open(image_path).convert("RGBA")
    rounded_image = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

    # Create a mask with rounded corners
    mask = Image.new("L", original_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), original_image.size], corner_radius, fill=255)
    rounded_image.putalpha(mask)

    # Paste the original image onto the rounded image using the mask
    rounded_image.paste(original_image, (0, 0), mask)

    # Resize the image to the desired output size
    rounded_image = rounded_image.resize(output_size, Image.Resampling.LANCZOS)

    # Convert the rounded image to PhotoImage
    rounded_image_tk = ImageTk.PhotoImage(rounded_image)

    return rounded_image_tk

# Function to connect to the database and fetch data
def fetch_data():
    try:
        connection = mysql.connector.connect(**db_config.db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        data = cursor.fetchall()

        return data

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to open the profile window and close the homepage window
def open_profile(username):
    my_profile.profile_page(username)
    #hpage.destroy()  # Close the homepage window

# Function to display fetched data using customtkinter
def display_data(data):
    global hpage  # Declare hpage as a global variable
    if not data:
        return

     # Selecting GUI theme - dark, light, system (for system default)
    ctk.set_appearance_mode("light")

    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("blue")

    hpage = ctk.CTk()
    hpage.attributes('-fullscreen', True) 
    hpage.title("Daily Post Homepage")

    label = ctk.CTkLabel(hpage, text="Daily Post", font=("Ink Free", 50, "bold"), corner_radius=10)
    label.pack(pady=50)

    frame = ctk.CTkFrame(master=hpage, border_width=2, corner_radius=10, height=50)
    frame.pack(pady=20, padx=40, fill="both" , expand=True)

    scrollbar = ctk.CTkScrollableFrame(master=frame, orientation='vertical')
    scrollbar.pack(fill='both', expand=True)

    add_post_button = ctk.CTkButton(hpage, text="Add Post", font=("Ink Free", 20, "bold"), command=add_post_window, width=20, height=2)
    add_post_button.place(relx=0.92, rely=0.05, anchor='ne')

    my_post_button = ctk.CTkButton(hpage, text="My Posts", font=("Ink Free", 20, "bold"), width=20, height=2)
    my_post_button.place(relx=0.1, rely=0.05, anchor='ne')

    my_post_button = ctk.CTkButton(hpage, text="My Profile", font=("Ink Free", 20, "bold"), width=20, height=2, command=lambda: open_profile(username))#my_profile.profile_page(username))
    my_post_button.place(relx=0.17, rely=0.05, anchor='ne')

    logout_button = ctk.CTkButton(hpage, text="Logout", font=("Ink Free", 20, "bold"), width=20, height=2, command=lambda: logout.logout_page(hpage), fg_color='#FFA500')  # Use the color code for yellowish-orange background button
    logout_button.place(relx=0.97, rely=0.05, anchor='ne')


    for row in data:
        image_path = row[1]  # Replace with the column index for the image path
        #text_data = format_text(row[2])   # Replace with the column index for the text data
        text_data = row[2]
        user_name = row[3]

        # for username
        user_label = ctk.CTkLabel(master=scrollbar, text=user_name,font= ("Times",20,"bold"))
        user_label.pack(side='top', anchor='w', padx=450, pady=5)

        rounded_image_tk = round_corners(image_path, 25, (576,324))
        rounded_image_pil = ImageTk.getimage(rounded_image_tk)

        my_image = ctk.CTkImage(light_image=rounded_image_pil,
                                dark_image=rounded_image_pil,
                                size=(576,324))
        
        # Create a label to display the image
        image_label = ctk.CTkLabel(master=scrollbar,text="", image=my_image)
        #image_label.pack(side='top', anchor='w', padx=100)
        image_label.pack(padx=100)

        # Display only a portion of text_data with link to show full text
        truncated_text = text_data[:300]  # Display the first 100 characters (adjust as needed)
        text_label = ctk.CTkLabel(master=scrollbar, text=truncated_text+"...read more", cursor='hand2', text_color='black', font=("Calibri Body", 16, "normal"), justify='left', wraplength=600)
        #text_label.bind("<Button-1>", lambda event, data=text_data: show_full_text(data))
        text_label.bind("<Button-1>", lambda event, data=text_data, image_path=image_path: show_full_text(data, image_path))
        text_label.pack(padx=100)
        
        def show_full_text(full_text, image_path):
            full_text_window = ctk.CTk()
            full_text_window.title("Full Text")
            '''
            print(image_path, full_text)

            # Load and display the image
            rounded_image_tk1 = round_corners(image_path, 25, (576, 324))
            rounded_image_pil1 = ImageTk.PhotoImage(rounded_image_tk1)
            #rounded_image_pil1 = ImageTk.getimage(rounded_image_tk1)
            my_image1 = ctk.CTkImage(light_image=rounded_image_pil1,
                                    dark_image=rounded_image_pil1,
                                    size=(576, 324))
            
            full_image_label = ctk.CTkLabel(full_text_window, text="", image=my_image1)
            full_image_label.pack(pady=10)
            '''
            # Display the full text
            full_text_label = ctk.CTkLabel(full_text_window, text=full_text, text_color='black', font=("Calibri Body", 16, "normal"), justify='left', wraplength=600)
            full_text_label.pack(pady=10, padx=10)

            full_text_window.mainloop()


    hpage.mainloop()

def format_text(text_data):
    # Split the text into paragraphs using newline characters
    paragraphs = text_data.split('\n\n')
    formatted_text = ""

    # Add HTML markup to format the text
    for paragraph in paragraphs:
        # Check for headings (lines starting with '#')
        if paragraph.startswith('#'):
            heading = paragraph.strip('#').strip()
            formatted_text += f"<h2>{heading}</h2>"
        else:
            # Add paragraphs with bold text
            formatted_text += f"<p><b>{paragraph}</b></p>"

    return formatted_text

# Function to add a post using a separate window
def add_post_window():

    global hpage  # Declare hpage as a global variable
    
    add_post_window = ctk.CTk()
     # Set the width and height of the window to be half the screen
    #window_width = add_post_window.winfo_screenwidth() // 2
    #window_height = add_post_window.winfo_screenheight() // 2
    #add_post_window.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
    add_post_window.attributes('-fullscreen', True) 
    add_post_window.title("Add New Post")

    # Adjusted label with bigger text and changed font
    label = ctk.CTkLabel(add_post_window, text="Daily Post", font=("Ink Free", 100, "bold"), corner_radius=20)
    label.pack(pady=100)

    selected_image_path = ""
    formatted_path = ""

    # Function to handle the "Select Photo" button click
    def select_photo():
        nonlocal selected_image_path
        nonlocal formatted_path
        if hpage:
            hpage.destroy()
        selected_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        formatted_path = selected_image_path.replace('/', '\\')
        print(formatted_path)
        image_path_entry.delete(0, END)
        image_path_entry.insert(0, selected_image_path)

    # Function to handle the "Add Post" button click
    def add_post_in_window():
        new_text_data = text_entry.get()
        # Validate that all required fields are filled
        if selected_image_path and new_text_data: #and new_user_name:
            # Call the insert_post function to add the new post to the database
            insert_post(selected_image_path, new_text_data)
            add_post_window.destroy()
            fetched_data = fetch_data()
            display_data(fetched_data)

            

    # Create and pack widgets for the "Add New Post" window
    ctk.CTkButton(add_post_window, text="Select Photo", command=select_photo, font=("Ink Free", 16, "bold")).pack(pady=5)

    ctk.CTkLabel(add_post_window, text="Image Path:", font=("Ink Free", 16, "bold")).pack(pady=5)
    image_path_entry = ctk.CTkEntry(add_post_window, font=("Ink Free", 16, "bold"), width=100)
    image_path_entry.pack(pady=5)
    '''
    rounded_image_tk_small = round_corners(formatted_path, 5, (72,40.5))
    rounded_image_pil_small = ImageTk.getimage(rounded_image_tk_small)

    my_image_small = ctk.CTkImage(light_image=rounded_image_pil_small,
                                dark_image=rounded_image_pil_small,
                                size=(72,40.5))
        
    # Create a label to display the image
    image_label = ctk.CTkLabel(add_post_window,text="", image=my_image_small)
    image_label.pack(padx=100)
    '''
    ctk.CTkLabel(add_post_window, text="Text Data:", font=("Ink Free", 16, "bold")).pack(pady=5)
    text_entry = ctk.CTkEntry(add_post_window, font=("Ink Free", 16, "bold"), width=100)
    text_entry.pack(pady=5)

    #ctk.CTkLabel(add_post_window, text="User Name:", font=("Arial", 12)).pack(pady=5)
    #user_name_entry = ctk.CTkEntry(add_post_window, font=("Arial", 12), width=40)
    #user_name_entry.pack(pady=5)

    ctk.CTkButton(add_post_window, text="Add Post", font=("Ink Free", 16, "bold"), command=add_post_in_window).pack(pady=10)

    add_post_window.mainloop()

# Fetch data from the database
fetched_data = fetch_data()

# Display the fetched data using customtkinter
display_data(fetched_data)

