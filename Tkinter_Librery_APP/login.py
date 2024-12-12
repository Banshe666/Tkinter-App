import customtkinter as ctk  # CustomTkinter for modern GUI design with tkinter.
from PIL import Image, UnidentifiedImageError  # Module to load and handle images.
import tkinter.messagebox as messagebox  # Module for displaying message boxes.
import sqlite3  # SQLite3 for database management.
import subprocess  # Module to execute external scripts or programs.
from functions import exit_command  # Custom function to handle exit operations.

# -------------------------------------------
# Function: login_screen_main
# Purpose:
# This function creates and manages the main login window.
# It handles user input for username and password, validates credentials
# against the SQLite database, and transitions to the main application upon successful login.
# -------------------------------------------
def login_screen_main():
    # Block: Initialize Login Window
    # Creates the main login window with fixed size and no borders.
    login_root = ctk.CTk()  # Main window instance.
    login_root.geometry("850x450")  # Set window size.
    login_root.resizable(False, False)  # Disable window resizing.
    login_root.config(bg='#aa965b')  # Set background color.
    login_root.overrideredirect(True)  # Remove window borders and title bar.

    # Block: Center Window on Screen
    # Centers the login window on the user's display.
    screen_width = login_root.winfo_screenwidth()  # Retrieve screen width.
    screen_height = login_root.winfo_screenheight()  # Retrieve screen height.
    window_width = 850  # Width of the login window.
    window_height = 450  # Height of the login window.
    pos_x = (screen_width // 2) - (window_width // 2)  # Calculate X position.
    pos_y = (screen_height // 2) - (window_height // 2)  # Calculate Y position.
    login_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')  # Apply position to window.

    # Block: Enable Window Dragging
    # Allows the user to drag the window by clicking and holding the mouse.
    def start_move(event):
        """Stores the initial position when the mouse button is pressed."""
        login_root.x = event.x
        login_root.y = event.y

    def stop_move(event):
        """Resets the stored positions when the mouse button is released."""
        login_root.x = None
        login_root.y = None

    def do_move(event):
        """Calculates and updates the window position as the mouse is dragged."""
        deltax = event.x - login_root.x  # Change in X position.
        deltay = event.y - login_root.y  # Change in Y position.
        x = login_root.winfo_x() + deltax  # New X coordinate.
        y = login_root.winfo_y() + deltay  # New Y coordinate.
        login_root.geometry(f"+{x}+{y}")  # Update window position.

    # Bind mouse events to enable window dragging.
    login_root.bind("<ButtonPress-1>", start_move)
    login_root.bind("<ButtonRelease-1>", stop_move)
    login_root.bind("<B1-Motion>", do_move)

    # -------------------------------------------
    # Function: load_background_image
    # Purpose:
    # Attempts to load the background image for the login screen.
    # If the image is not found or is invalid, it displays an error message.
    # -------------------------------------------
    def load_background_image():
        try:
            login_image = ctk.CTkImage(
                light_image=Image.open('./images/login_background.jpg'),  # Light mode image.
                dark_image=Image.open('./images/login_background.jpg'),   # Dark mode image.
                size=(850, 450)  # Set image size to match window.
            )
            return login_image
        except (FileNotFoundError, UnidentifiedImageError):
            messagebox.showerror("Error", "Image Not Found.")  # Display error if image fails to load.
            return None

    # Block: Set Background Image
    # Applies the background image if available; otherwise, uses the default background color.
    login_image = load_background_image()
    if login_image:
        login_image_label = ctk.CTkLabel(
            login_root, text='', image=login_image, bg_color='#aa965b'
        )
        login_image_label.place(x=0, y=0)  # Position the background image.
    else:
        login_root.config(bg='#aa965b')  # Fallback to default background color.

    # Block: Initialize User Input Variables
    # Variables to store the username and password entered by the user.
    username_var = ctk.StringVar()  # Variable for username input.
    password_var = ctk.StringVar()  # Variable for password input.

    # -------------------------------------------
    # Function: on_focus_in
    # Purpose:
    # Clears the placeholder text when the entry field gains focus.
    # Optionally masks input if it's a password field.
    # -------------------------------------------
    def on_focus_in(event, entry, placeholder, is_password=False):
        if entry.get() == placeholder:
            entry.delete(0, "end")  # Remove placeholder text.
            entry.configure(text_color='black')  # Set text color to black.
            if is_password:
                entry.configure(show='*')  # Mask password input.

    # -------------------------------------------
    # Function: on_focus_out
    # Purpose:
    # Restores the placeholder text if the entry field is left empty.
    # Optionally unmasks input if it's a password field.
    # -------------------------------------------
    def on_focus_out(event, entry, placeholder, is_password=False):
        if entry.get() == "":
            entry.insert(0, placeholder)  # Insert placeholder text.
            entry.configure(text_color='grey')  # Set text color to grey.
            if is_password:
                entry.configure(show='')  # Unmask password input.

    # Block: Create Username Entry Field
    # Sets up the entry field for the user to input their username.
    user_login_entry = ctk.CTkEntry(
        login_root,
        textvariable=username_var,  # Bind to username_var.
        width=250,  # Width of the entry field.
        height=30,  # Height of the entry field.
        fg_color="white",  # Foreground color.
        text_color='black',  # Text color.
        border_color='black',  # Border color.
        bg_color='#aa965b',  # Background color.
        placeholder_text_color='black',  # Placeholder text color.
        font=('Cascadia Code', 12)  # Font style and size.
    )
    user_login_entry.insert(0, 'Enter your username:')  # Set placeholder text.
    # Bind focus events to handle placeholder behavior.
    user_login_entry.bind("<FocusIn>", lambda event: on_focus_in(event, user_login_entry, 'Enter your username:'))
    user_login_entry.bind("<FocusOut>", lambda event: on_focus_out(event, user_login_entry, 'Enter your username:'))
    user_login_entry.place(x=300, y=150)  # Position the username entry field.

    # Block: Create Password Entry Field
    # Sets up the entry field for the user to input their password.
    user_pass_entry = ctk.CTkEntry(
        login_root,
        textvariable=password_var,  # Bind to password_var.
        placeholder_text='Enter your password:',  # Placeholder text.
        width=250,  # Width of the entry field.
        height=30,  # Height of the entry field.
        fg_color="white",  # Foreground color.
        text_color='black',  # Text color.
        border_color='black',  # Border color.
        bg_color='#aa965b',  # Background color.
        placeholder_text_color='black',  # Placeholder text color.
        font=('Cascadia Code', 12),  # Font style and size.
        show=''  # Initially show text (no masking).
    )
    user_pass_entry.insert(0, 'Enter your password:')  # Set placeholder text.
    # Bind focus events to handle placeholder behavior and password masking.
    user_pass_entry.bind("<FocusIn>", lambda event: on_focus_in(event, user_pass_entry, 'Enter your password:', is_password=True))
    user_pass_entry.bind("<FocusOut>", lambda event: on_focus_out(event, user_pass_entry, 'Enter your password:', is_password=True))
    user_pass_entry.place(x=300, y=200)  # Position the password entry field.

    # Block: Create Error Message Label
    # Label to display error messages when login fails.
    miss_data = ctk.CTkLabel(
        login_root,
        text='Wrong Username or Password',  # Error message text.
        text_color='red',  # Text color.
        bg_color='#aa965b',  # Background color.
        fg_color='white',  # Foreground color.
        font=('Cascadia Code', 12)  # Font style and size.
    )

    # -------------------------------------------
    # Function: validate_credentials
    # Purpose:
    # Retrieves the entered username and password, validates them against
    # the SQLite database, and proceeds to the main application if valid.
    # Displays an error message if validation fails.
    # -------------------------------------------
    def validate_credentials():
        username = username_var.get()  # Get the entered username.
        password = password_var.get()  # Get the entered password.

        # Check if both fields are filled.
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        # Database connection details.
        db_path = './db/bookstore_management.db'  # Path to the SQLite database.
        table_name = 'usuarios'  # Name of the user table.
        username_column = 'nombre_usuario'  # Column name for username.
        password_column = 'password'  # Column name for password.

        try:
            conn = sqlite3.connect(db_path)  # Connect to the database.
            cursor = conn.cursor()  # Create a cursor object.

            # SQL query to select user with matching username and password.
            query = f"""
            SELECT * FROM "{table_name}"
            WHERE "{username_column}" = ? AND "{password_column}" = ?
            """
            cursor.execute(query, (username, password))  # Execute the query with parameters.
            result = cursor.fetchone()  # Fetch the first matching record.
            conn.close()  # Close the database connection.

            if result:
                # If credentials are valid, launch the main application.
                subprocess.Popen(["pythonw", "main_data.py", username_var.get()], creationflags=subprocess.CREATE_NO_WINDOW)
                login_root.destroy()  # Close the login window.
            else:
                # If credentials are invalid, display the error message.
                miss_data.place(x=300, y=240)
        except sqlite3.Error as e:
            # Show a database error message if an exception occurs.
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Block: Create Login Button
    # Button to initiate credential validation.
    login_button = ctk.CTkButton(
        login_root,
        text='Sign in',  # Button text.
        width=250,  # Button width.
        height=30,  # Button height.
        border_color='black',  # Border color.
        bg_color='white',  # Background color.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Color on hover.
        font=('Cascadia Code', 12),  # Font style and size.
        command=validate_credentials  # Function to call on click.
    )
    login_button.place(x=300, y=280)  # Position the login button.

    # Block: Create Exit Button
    # Button to close the application.
    login_exit_button = ctk.CTkButton(
        login_root,
        text='Exit',  # Button text.
        width=50,  # Button width.
        height=30,  # Button height.
        border_color='black',  # Border color.
        bg_color='white',  # Background color.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Color on hover.
        font=('Cascadia Code', 12),  # Font style and size.
        command=lambda: exit_command(login_root)  # Exit command function.
    )
    login_exit_button.place(x=500, y=350)  # Position the exit button.

    # -------------------------------------------
    # Function: on_enter_key
    # Purpose:
    # Triggers credential validation when the Enter key is pressed.
    # -------------------------------------------
    def on_enter_key(event):
        if username_var.get() and password_var.get():
            validate_credentials()  # Call the validation function.

    # Block: Bind Enter Key
    # Allows the user to press Enter to submit the login form.
    login_root.bind('<Return>', on_enter_key)  # Bind the Enter key to the handler.

    # Block: Start Main Event Loop
    # Initiates the Tkinter event loop to run the login screen.
    login_root.mainloop()  # Start the Tkinter event loop.

# -------------------------------------------
# Execution: Start Login Screen
# Purpose:
# Calls the main function to initialize and display the login screen.
# -------------------------------------------
login_screen_main()
