# Function to create an exit confirmation window when attempting to close the application
def exit_command(login_root):

    # Creates a new top-level window for the exit confirmation
    exit_screen = ctk.CTkToplevel(login_root)
    exit_screen.geometry("250x150")
    exit_screen.title("Exit Window")
    exit_screen.config(bg="#8C6846")
    exit_screen.resizable(False, False)
    exit_screen.grab_set()  # Ensures the user interacts only with this window
    exit_screen.focus_force()

    # Center the exit confirmation window on the screen
    screen_width = exit_screen.winfo_screenwidth()
    screen_height = exit_screen.winfo_screenheight()
    window_width = 250
    window_height = 150
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    exit_screen.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')
    exit_screen.after(200, lambda: exit_screen.iconbitmap('./images/icobookstore.ico'))

    # Function to confirm exit and close the main application window
    def ok_button():
        login_root.destroy()

    # Function to cancel and close the exit confirmation window
    def cancel_button():
        exit_screen.destroy()

    # Add a label with the exit confirmation question
    ask_label = ctk.CTkLabel(exit_screen,
                             text='Do you wanna close the app?',
                             bg_color="#8C6846",
                             text_color='white',
                             font=('Cascadia Code', 14))
    ask_label.place(x=15, y=50)

    # Add an "OK" button to confirm exit
    ok_button = ctk.CTkButton(exit_screen,
                              text='OK',
                              bg_color='#8C6846',
                              command=ok_button,
                              width=50,
                              height=30,
                              font=('Cascadia Code', 14),
                              fg_color='#605b3e',
                              hover_color='#9fa081')
    ok_button.place(x=50, y=110)

    # Add a "Cancel" button to close the exit confirmation window
    cancel_button = ctk.CTkButton(exit_screen,
                                  text='Cancel',
                                  bg_color='#8C6846',
                                  command=cancel_button,
                                  width=30,
                                  height=30,
                                  font=('Cascadia Code', 14),
                                  fg_color='#605b3e',
                                  hover_color='#9fa081')
    cancel_button.place(x=150, y=110)

# Functions to enable window dragging functionality

# Initiates the move operation by capturing the offset of the mouse pointer
def start_move(event, root):
    root._offsetx = event.x
    root._offsety = event.y

# Stops the move operation by resetting the offset
def stop_move(event, root):
    root._offsetx = None
    root._offsety = None

# Moves the window based on the current mouse position and the captured offset
def do_move(event, root):
    if root._offsetx is not None and root._offsety is not None:
        x = event.x_root - root._offsetx
        y = event.y_root - root._offsety
        root.geometry(f"+{x}+{y}")
