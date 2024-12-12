import customtkinter as ctk  # CustomTkinter for modern GUI design with tkinter.
from PIL import Image, UnidentifiedImageError  # Module to load and handle images.
import subprocess  # Module to execute external scripts or programs.
import sqlite3  # SQLite3 for database management.
import os  # Module to interact with the file system.

# -------------------------------------------
# Function: splash_screen_main
# Purpose:
# This function creates and manages a splash screen window. It displays a background image,
# checks for database connectivity, and then launches the next script (e.g., login window).
# -------------------------------------------
def splash_screen_main():
    # Block: Initialize Splash Screen Window
    # Creates a splash screen window with fixed size and no borders.
    splash_root = ctk.CTk()
    splash_root.geometry('400x400')
    splash_root.resizable(False, False)
    splash_root.overrideredirect(True)

    # Block: Center Window on Screen
    # Centers the splash screen window on the user's display.
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    window_width = 400
    window_height = 400
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    splash_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    # Block: Message Label for Errors/Status
    splash_label_msg = ctk.CTkLabel(
        splash_root,
        text=' ',
        bg_color='#4C2C17',
        fg_color='#4C2C17',
        font=('Arial', 14)
    )
    splash_label_msg.place(x=70, y=350)

    # -------------------------------------------
    # Function: load_background_image
    # Purpose:
    # Attempts to load the background image for the splash screen.
    # If not found or invalid, it displays an error message.
    # -------------------------------------------
    def load_background_image():
        try:
            splash_imagen_center = ctk.CTkImage(
                light_image=Image.open('./images/fondo_splash.jpg'),
                dark_image=Image.open('./images/fondo_splash.jpg'),
                size=(400, 400)
            )
            return splash_imagen_center
        except (FileNotFoundError, UnidentifiedImageError):
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

    # Block: Load Background Image
    splash_imagen_center = load_background_image()
    if splash_imagen_center:
        splash_image_properties = ctk.CTkLabel(
            splash_root,
            text='',
            image=splash_imagen_center,
            bg_color='#080B1C'
        )
        splash_image_properties.place(x=0, y=0)

    splash_label_msg.lift()  # Ensures message label appears above background image.

    # -------------------------------------------
    # Function: check_db_connection
    # Purpose:
    # Verifies if the SQLite database file exists and connects successfully.
    # If successful, proceeds to the next step.
    # -------------------------------------------
    def check_db_connection():
        db_path = './db/bookstore_management.db'
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                conn.close()
                data_update_check()
            except sqlite3.Error:
                splash_label_msg.configure(text="Database connection failed.")
                splash_root.update_idletasks()
                splash_root.after(2000, splash_root.destroy)
        else:
            splash_label_msg.configure(text="Database not found.")
            splash_root.update_idletasks()
            splash_root.after(2000, splash_root.destroy)

    # -------------------------------------------
    # Function: start_reconocimiento
    # Purpose:
    # Simulates an initial recognition process before checking the database.
    # -------------------------------------------
    def start_reconocimiento():
        splash_root.update_idletasks()
        splash_root.after(1000, check_db_connection)

    # -------------------------------------------
    # Function: data_update_check
    # Purpose:
    # Simulates a data update process before opening the next script.
    # -------------------------------------------
    def data_update_check():
        splash_root.update_idletasks()
        splash_root.after(1000, open_next_script)

    # -------------------------------------------
    # Function: open_next_script
    # Purpose:
    # Launches the login window script and closes the splash screen.
    # -------------------------------------------
    def open_next_script():
        subprocess.Popen(["pythonw", "login.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        splash_root.destroy()

    # Block: Start Splash Screen Logic
    splash_root.after(1000, start_reconocimiento)

    # Block: Run Main Loop
    splash_root.mainloop()

# Call Main Function to Start Splash Screen
splash_screen_main()
