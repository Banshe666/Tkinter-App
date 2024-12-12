import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
import tkinter.messagebox as messagebox
import sqlite3
import subprocess
from functions import exit_command


# Function to display the login screen
def login_screen_main():
    # Create the main login window
    login_root = ctk.CTk()
    login_root.geometry("850x450")
    login_root.resizable(False, False)
    login_root.config(bg='#aa965b')
    login_root.overrideredirect(True)  # Remove borders and title bar

    # Center the login window on the screen
    screen_width = login_root.winfo_screenwidth()
    screen_height = login_root.winfo_screenheight()
    window_width = 850
    window_height = 450
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    login_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    # Enable dragging the window
    def start_move(event):
        login_root.x = event.x
        login_root.y = event.y

    def stop_move(event):
        login_root.x = None
        login_root.y = None

    def do_move(event):
        deltax = event.x - login_root.x
        deltay = event.y - login_root.y
        x = login_root.winfo_x() + deltax
        y = login_root.winfo_y() + deltay
        login_root.geometry(f"+{x}+{y}")

    login_root.bind("<ButtonPress-1>", start_move)
    login_root.bind("<ButtonRelease-1>", stop_move)
    login_root.bind("<B1-Motion>", do_move)

    # Load background image for the login screen
    def load_background_image():
        try:
            login_image = ctk.CTkImage(
                light_image=Image.open('./images/login_background.jpg'),
                dark_image=Image.open('./images/login_background.jpg'),
                size=(850, 450)
            )
            return login_image
        except (FileNotFoundError, UnidentifiedImageError):
            messagebox.showerror("Error", "Image Not Found.")
            return None

    # Set background image if available, otherwise use default color
    login_image = load_background_image()
    if login_image:
        login_image_label = ctk.CTkLabel(
            login_root, text='', image=login_image, bg_color='#aa965b'
        )
        login_image_label.place(x=0, y=0)
    else:
        login_root.config(bg='#aa965b')

    # Variables for username and password
    username_var = ctk.StringVar()
    password_var = ctk.StringVar()

    # Placeholder behavior for entry fields
    def on_focus_in(event, entry, placeholder, is_password=False):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.configure(text_color='black')
            if is_password:
                entry.configure(show='*')

    def on_focus_out(event, entry, placeholder, is_password=False):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(text_color='grey')
            if is_password:
                entry.configure(show='')

    # Entry field for username
    user_login_entry = ctk.CTkEntry(
        login_root,
        textvariable=username_var,
        width=250,
        height=30,
        fg_color="white",
        text_color='black',
        border_color='black',
        bg_color='#aa965b',
        placeholder_text_color='black',
        font=('Cascadia Code', 12)
    )
    user_login_entry.insert(0, 'Enter your username:')
    user_login_entry.bind("<FocusIn>", lambda event: on_focus_in(event, user_login_entry, 'Enter your username:'))
    user_login_entry.bind("<FocusOut>", lambda event: on_focus_out(event, user_login_entry, 'Enter your username:'))
    user_login_entry.place(x=300, y=150)

    # Entry field for password
    user_pass_entry = ctk.CTkEntry(
        login_root,
        textvariable=password_var,
        placeholder_text='Enter your password:',
        width=250,
        height=30,
        fg_color="white",
        text_color='black',
        border_color='black',
        bg_color='#aa965b',
        placeholder_text_color='black',
        font=('Cascadia Code', 12),
        show=''
    )
    user_pass_entry.insert(0, 'Enter your password:')
    user_pass_entry.bind("<FocusIn>", lambda event: on_focus_in(event, user_pass_entry, 'Enter your password:', is_password=True))
    user_pass_entry.bind("<FocusOut>", lambda event: on_focus_out(event, user_pass_entry, 'Enter your password:', is_password=True))
    user_pass_entry.place(x=300, y=200)

    # Label for login error message
    miss_data = ctk.CTkLabel(
        login_root,
        text='Wrong Username or Password',
        text_color='red',
        bg_color='#aa965b',
        fg_color='white',
        font=('Cascadia Code', 12)
    )

    # Function to validate credentials against the database
    def validate_credentials():
        username = username_var.get()
        password = password_var.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        db_path = './db/bookstore_management.db'
        table_name = 'usuarios'
        username_column = 'nombre_usuario'
        password_column = 'password'

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = f"""
            SELECT * FROM "{table_name}"
            WHERE "{username_column}" = ? AND "{password_column}" = ?
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                subprocess.Popen(["pythonw", "main_data.py", username_var.get()], creationflags=subprocess.CREATE_NO_WINDOW)
                login_root.destroy()
            else:
                miss_data.place(x=300, y=240)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")



    # Login button
    login_button = ctk.CTkButton(
        login_root,
        text='Sign in',
        width=250,
        height=30,
        border_color='black',
        bg_color='white',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 12),
        command=validate_credentials
    )
    login_button.place(x=300, y=280)

    # Exit button
    login_exit_button = ctk.CTkButton(
        login_root,
        text='Exit',
        width=50,
        height=30,
        border_color='black',
        bg_color='white',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 12),
        command=lambda: exit_command(login_root)
    )
    login_exit_button.place(x=500, y=350)

    # Bind Enter key to login validation
    def on_enter_key(event):
        if username_var.get() and password_var.get():
            validate_credentials()

    login_root.bind('<Return>', on_enter_key)

    # Run the login screen's event loop
    login_root.mainloop()

login_screen_main()
