import customtkinter as ctk
from tkinter import *
from PIL import ImageTk
from tkinter import filedialog
import os
import logouttk
import my_profiletk
import tkinter as tk
from functionstk import *
from img_modstk import *
import tkinter.messagebox as messagebox
from commentstk import *
from searchtk import search_posts

username = os.environ.get("USERNAME")  # Retrieve environment variable
print("Welcome "+ username)
hpage = None

# Function to open the profile window and close the homepage window
def open_profile(username):
    hpage.destroy()
    my_profiletk.profile_page(username)
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

    hpage = tk.Tk()
    hpage.attributes('-fullscreen', True) 
    hpage.title("Daily Post Homepage")

    label = Label(hpage, text="Daily Post", font=("Ink Free", 50, "bold"))
    label.pack(pady=40)
    
    #my_post_button = Button(hpage, text="My Posts", font=("Ink Free", 20, "bold"))
    #my_post_button.place(relx=0.12, rely=0.05, anchor='ne')

    my_post_button = Button(hpage, text="My Account", font=("Ink Free", 20, "bold"), command=lambda: open_profile(username))
    my_post_button.place(relx=0.13, rely=0.05, anchor='ne')

    # Search field and icon
    search_frame = Frame(hpage)
    search_frame.place(relx=0.34, rely=0.065, anchor='ne')

    search_entry = Entry(search_frame, font=("Ink Free", 16, "bold"))
    search_entry.pack(side=LEFT)

    global search_results_menu
    search_results_menu = Menu(search_frame, tearoff=0)  # Create a dropdown menu for search results

    def handle_enter(event):
        entered = search_entry.get()
        perform_search(entered)

    search_entry.bind("<Return>", handle_enter)

    search_icon_label = Label(search_frame, text="🔍", cursor='hand2', font=("Ink Free", 16))
    search_icon_label.bind("<Button-1>", lambda event: perform_search(search_entry.get())) 
    search_icon_label.pack(side=LEFT)

    def perform_search(query):
        global search_results_menu
        search_results_menu.delete(0, END)  # Clear previous search results
        results = search_posts(query)

        if results:
            for post in results:
                search_results_menu.add_command(label=post, command=lambda p=post: print(p))  # Add each post as a menu item
            search_results_menu.post(search_frame.winfo_rootx(), search_frame.winfo_rooty() + search_frame.winfo_height())  # Display the dropdown menu
        else:
            print("No results found")



    add_post_button = Button(hpage, text="Add Post", font=("Ink Free", 20, "bold"), command=add_post_window)
    add_post_button.place(relx=0.894, rely=0.05, anchor='ne')
    
    logout_button = Button(hpage, text="Logout", font=("Ink Free", 20, "bold"), command=lambda: logouttk.logout_page(hpage))
    logout_button.place(relx=0.97, rely=0.05, anchor='ne')

    frame = Frame(master=hpage, borderwidth=2, height=50, relief="groove")
    frame.pack(pady=20, padx=40, fill="both" , expand=True)

    scrollbar = ctk.CTkScrollableFrame(master=frame, orientation='vertical')
    scrollbar.pack(fill='both', expand=True)

    for row in data:
        image_path = row[1]  # Replace with the column index for the image path
        #text_data = format_text(row[2])   # Replace with the column index for the text data
        text_data = row[2]
        user_name = row[3]
        heading = row[4]
        
        # for username
        user_label = ctk.CTkLabel(master=scrollbar, text=user_name,font= ("Ink Free",25,"bold"))
        user_label.pack(side='top', anchor='w', padx=450, pady=5)
        #user_label.grid(row=0, column=0, padx=100, pady=5)

        rounded_image_tk = round_corners(image_path, 25, (576,324))
        rounded_image_pil = ImageTk.getimage(rounded_image_tk)

        my_image = ctk.CTkImage(light_image=rounded_image_pil,
                                dark_image=rounded_image_pil,
                                size=(576,324))
        
        # Create a label to display the image
        image_label = ctk.CTkLabel(master=scrollbar,text="", image=my_image)
        #image_label.pack(side='top', anchor='w', padx=100)
        image_label.pack(padx=100)
        #image_label.grid(row=0, column=0, padx=100) 
        '''
        # Display only a portion of text_data with link to show full text
        truncated_text = text_data[:100]  # Display the first 100 characters (adjust as needed)
        text_label = ctk.CTkLabel(master=scrollbar, text=truncated_text+"...read more", cursor='hand2', text_color='black', font=("Calibri Body", 16, "normal"), justify='left', wraplength=600)
        #text_label.bind("<Button-1>", lambda event, data=text_data: show_full_text(data))
        text_label.bind("<Button-1>", lambda event, data=text_data, image_path=image_path: show_full_text(data, image_path))
        text_label.pack(padx=100)
        #text_label.grid(row=1, column=1, padx=100) 
        '''       
        if len(heading)>=35:
            trunc_heading=heading[:35]

            heading_label=ctk.CTkLabel(master=scrollbar, text=trunc_heading+"...read more", cursor='hand2', text_color='black', font=("Cascadia Code", 16, "bold"), justify='left')
            heading_label.bind("<Button-1>", lambda event, data=text_data, image_path=image_path: show_full_text(data, image_path))
            heading_label.pack(side='top', anchor='w', padx=450)
        else:
            heading_label=ctk.CTkLabel(master=scrollbar, text=heading+"...read more", cursor='hand2', text_color='black', font=("Cascadia Code", 16, "bold"), justify='left')
            heading_label.bind("<Button-1>", lambda event, data=text_data, image_path=image_path: show_full_text(data, image_path))
            heading_label.pack(side='top', anchor='w', padx=450)

        comment_label=ctk.CTkLabel(master=scrollbar, text="View all comments", cursor='hand2', text_color='black', font=("Cascadia Code", 16, "bold"))
        comment_label.bind("<Button-1>", lambda event, id=row[0]: display_comments(id,username))
        comment_label.pack(side='top', anchor='w', padx=450)

        def show_full_text(full_text, image_path):
            full_text_window = tk.Tk()
            #full_text_window.attributes('-fullscreen', True)
            # Set the width and height of the window to be half the screen
            window_width = full_text_window.winfo_screenwidth() // 2
            window_height = full_text_window.winfo_screenheight() // 2
            full_text_window.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
            full_text_window.title("Full Text")
            
            frame = Frame(master=full_text_window, borderwidth=5, height=50, relief="groove")
            frame.pack(pady=20, padx=40, fill="both" , expand=True)

            scrollbar = ctk.CTkScrollableFrame(master=frame, orientation='vertical')
            scrollbar.pack(fill='both', expand=True)
            print("Image path:", image_path)
            
            try:
                # Load and display the image
                rounded_image_tk1 = round_corners(image_path, 25, (576, 324))
                rounded_image_pil1 = ImageTk.getimage(rounded_image_tk1)

                # Verify the image data
                print("PIL Image:", rounded_image_pil1)

                my_image1 = ctk.CTkImage(light_image=rounded_image_pil1,
                                        dark_image=rounded_image_pil1,
                                        size=(576, 324))

                # Check the created image object
                print(my_image1)

                full_image_label = ctk.CTkLabel(master=scrollbar, text="", image=my_image1)
                full_image_label.pack(pady=10)
            except Exception as e:
                print("Error loading image:", e)

            # Display the full text
            full_text_label = ctk.CTkLabel(master=scrollbar, text=full_text, text_color='black', font=("Calibri Body", 16, "normal"), justify='left', wraplength=600)
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
        #display_image(formatted_path)
        return formatted_path

    # Function to handle the "Add Post" button click
    def add_post_in_window():
        #new_text_data = save_content()
        new_text_data = text_entry.get("1.0", "end-1c")
        print("Content Saved:", new_text_data)
        # Validate that all required fields are filled
        if selected_image_path and new_text_data: #and new_user_name:
            # Call the insert_post function to add the new post to the database
            insert_post(selected_image_path, new_text_data)
            add_post_window.destroy()
            fetched_data = fetch_data()
            display_data(fetched_data)
    
    add_post_window = tk.Tk()
     # Set the width and height of the window to be half the screen
    #window_width = add_post_window.winfo_screenwidth() // 2
    #window_height = add_post_window.winfo_screenheight() // 2
    #add_post_window.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
    add_post_window.attributes('-fullscreen', True) 
    add_post_window.title("Add New Post")

    # Adjusted label with bigger text and changed font
    label = Label(add_post_window, text="Daily Post", font=("Ink Free", 50, "bold"))
    label.pack(pady=50)

    frame = tk.Frame(add_post_window, borderwidth=2)
    frame.pack(pady=20, padx=40)

    # Create and pack widgets for the "Add New Post" window
    tk.Button(frame, text="Select Photo", command=select_photo, font=("Ink Free", 16, "bold")).grid(row=1, column=0, pady=5)

    tk.Label(frame, width=30, text="Image Path:", font=("Ink Free", 16, "bold")).grid(row=2, column=0, pady=5)
    image_path_entry = tk.Entry(frame, font=("Ink Free", 16, "bold"), width=100)
    image_path_entry.grid(row=3, column=0, pady=5)

    tk.Label(frame, text="Text Data:", font=("Ink Free", 16, "bold")).grid(row=4, column=0, pady=5)
    text_entry = tk.Text(frame, font=("Ink Free", 16, "bold"), wrap="word", width=100, height=10)
    text_entry.grid(row=5, column=0, pady=10)

    tk.Button(frame, text="Add Post", font=("Ink Free", 16, "bold"), command=add_post_in_window).grid(row=6, column=0, pady=10)

    add_post_window.mainloop()

# Fetch data from the database
fetched_data = fetch_data()

# Display the fetched data using customtkinter
display_data(fetched_data)

