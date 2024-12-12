import customtkinter as ctk
from tkinter import messagebox
import sqlite3

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



def delete_item(main_root, tabla_information):

    conn = sqlite3.connect('./db/bookstore_management.db')
    cursor = conn.cursor()

    selected_item = tabla_information.selection()

    if selected_item:

        book_id = tabla_information.item(selected_item[0])['values'][0]


        message = messagebox.askyesno('Message', 'Do you want to delete this book?', parent=main_root)
        if message:
            try:

                cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
                conn.commit()


                cursor.execute("""
                    WITH Ordered AS (
                        SELECT rowid, book_id, ROW_NUMBER() OVER (ORDER BY book_id) AS new_id
                        FROM books
                    )
                    UPDATE books
                    SET book_id = (SELECT new_id FROM Ordered WHERE Ordered.rowid = books.rowid)
                """)
                conn.commit()


                refresh_table(tabla_information, cursor)

                messagebox.showinfo('Message', 'Book deleted successfully!', parent=main_root)
            except Exception as e:
                messagebox.showerror('Error', f"An error occurred: {e}", parent=main_root)
    else:
        messagebox.showinfo('Message', "No item selected", parent=main_root)


    conn.close()


def refresh_table(tabla_information, cursor):
    for row in tabla_information.get_children():
        tabla_information.delete(row)


    cursor.execute("SELECT book_id, book_name, book_publisher, author_name, book_year, book_genre, book_language, book_ISBN, book_quantity FROM books ORDER BY book_id")
    for row in cursor.fetchall():
        tabla_information.insert("", "end", values=row)

def deselect_item(event, tabla_information):
    if not tabla_information.winfo_containing(event.x_root, event.y_root) == tabla_information:
        tabla_information.selection_remove(tabla_information.selection())


# Function to update the welcome label with the username.
# Displays "Guest" if no username is provided.
def update_user_name_label(name_label, username):
    if username:
        name_label.configure(text=f"Welcome, {username.upper()}")
    else:
        name_label.configure(text="Welcome, Guest")