import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
import subprocess
import sqlite3
import os

# Function to display the splash screen
def splash_screen_main():
    # Create the splash screen window
    splash_root = ctk.CTk()
    splash_root.geometry('400x400')
    splash_root.resizable(False, False)
    splash_root.overrideredirect(True)  # Remove window borders and title bar

    # Center the splash screen window on the screen
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    window_width = 400
    window_height = 400
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    splash_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    # Label to display messages during splash screen
    splash_label_msg = ctk.CTkLabel(
        splash_root,
        text=' ',
        bg_color='#4C2C17',
        fg_color='#4C2C17',
        font=('Arial', 14)
    )
    splash_label_msg.place(x=70, y=350)

    # Function to load the splash screen background image
    def load_background_image():
        try:
            # Load the background image for the splash screen
            splash_imagen_center = ctk.CTkImage(
                light_image=Image.open('./images/fondo_splash.jpg'),
                dark_image=Image.open('./images/fondo_splash.jpg'),
                size=(400, 400)
            )
            return splash_imagen_center
        except (FileNotFoundError, UnidentifiedImageError):
            # Display error message if the image is not found or invalid
            error_label = ctk.CTkLabel(
                splash_root,
                text="Background image not found.",
                bg_color='#080B1C',
                fg_color='#FFFFFF',
                font=('Arial', 16),
                width=400,
                height=400
            )
            error_label.place(x=0, y=0)
            splash_root.update_idletasks()
            return None

    # Load the background image and set it if available
    splash_imagen_center = load_background_image()
    if splash_imagen_center:
        splash_image_properties = ctk.CTkLabel(
            splash_root,
            text='',
            image=splash_imagen_center,
            bg_color='#080B1C'
        )
        splash_image_properties.place(x=0, y=0)

    # Ensure the message label appears above the background image
    splash_label_msg.lift()

    # Function to check the database connection
    def check_db_connection():
        db_path = './db/bookstore_management.db'
        if os.path.exists(db_path):
            try:
                # Attempt to connect to the database
                conn = sqlite3.connect(db_path)
                conn.close()
                data_update_check()  # Proceed to the next step if successful
            except sqlite3.Error:
                # Show error message if database connection fails
                splash_label_msg.configure(text="Database connection failed.")
                splash_root.update_idletasks()
                splash_root.after(2000, splash_root.destroy)
        else:
            # Show error message if the database file is not found
            splash_label_msg.configure(text="Database not found.")
            splash_root.update_idletasks()
            splash_root.after(2000, splash_root.destroy)

    # Function to simulate a recognition or loading process
    def start_reconocimiento():
        splash_root.update_idletasks()
        splash_root.after(1000, check_db_connection)

    # Function to check for data updates or other processes
    def data_update_check():
        splash_root.update_idletasks()
        splash_root.after(1000, open_next_script)

    # Function to open the next script (e.g., login window) after splash screen
    def open_next_script():
        subprocess.Popen(["python", "login.py"])
        splash_root.destroy()

    # Start the recognition process after 1 second
    splash_root.after(1000, start_reconocimiento())

    # Run the splash screen's event loop
    splash_root.mainloop()

splash_screen_main()
