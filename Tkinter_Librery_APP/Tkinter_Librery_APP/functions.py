import customtkinter as ctk  # CustomTkinter for modern GUI design with tkinter.
from tkinter import messagebox  # Module for displaying message boxes.
import sqlite3  # SQLite3 for database management.

# -------------------------------------------
# Function: exit_command
# Purpose:
# Creates and manages an exit confirmation window when the user attempts to close the application.
# Provides options to confirm exit or cancel the operation.
# -------------------------------------------
def exit_command(login_root):
    # Block: Initialize Exit Confirmation Window
    # Creates a new top-level window with specified size, appearance, and behavior.
    exit_screen = ctk.CTkToplevel(login_root)  # Exit confirmation window instance.
    exit_screen.geometry("250x150")  # Set window size.
    exit_screen.title("Exit Window")  # Set window title.
    exit_screen.config(bg="#8C6846")  # Set background color.
    exit_screen.resizable(False, False)  # Disable window resizing.
    exit_screen.grab_set()  # Ensure user interacts only with this window.
    exit_screen.focus_force()  # Focus on the exit confirmation window.

    # Block: Center Exit Window on Screen
    # Calculates and applies the position to center the window on the user's display.
    screen_width = exit_screen.winfo_screenwidth()  # Retrieve screen width.
    screen_height = exit_screen.winfo_screenheight()  # Retrieve screen height.
    window_width = 250  # Width of the exit window.
    window_height = 150  # Height of the exit window.
    pos_x = (screen_width // 2) - (window_width // 2)  # Calculate X position.
    pos_y = (screen_height // 2) - (window_height // 2)  # Calculate Y position.
    exit_screen.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')  # Apply position.
    exit_screen.after(200, lambda: exit_screen.iconbitmap('./images/icobookstore.ico'))  # Set window icon after 200ms.

    # -------------------------------------------
    # Function: ok_button
    # Purpose:
    # Confirms the exit action and closes the main application window.
    # -------------------------------------------
    def ok_button():
        login_root.destroy()  # Close the main application window.

    # -------------------------------------------
    # Function: cancel_button
    # Purpose:
    # Cancels the exit action and closes the exit confirmation window.
    # -------------------------------------------
    def cancel_button():
        exit_screen.destroy()  # Close the exit confirmation window.

    # Block: Add Exit Confirmation Label
    # Displays a message asking the user to confirm exiting the application.
    ask_label = ctk.CTkLabel(
        exit_screen,
        text='Do you wanna close the app?',  # Confirmation message text.
        bg_color="#8C6846",  # Background color.
        text_color='white',  # Text color.
        font=('Cascadia Code', 14)  # Font style and size.
    )
    ask_label.place(x=15, y=50)  # Position the confirmation label.

    # Block: Add "OK" Button
    # Button to confirm and proceed with exiting the application.
    ok_button = ctk.CTkButton(
        exit_screen,
        text='OK',  # Button text.
        bg_color='#8C6846',  # Background color.
        command=ok_button,  # Function to call on click.
        width=50,  # Button width.
        height=30,  # Button height.
        font=('Cascadia Code', 14),  # Font style and size.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#9fa081'  # Color on hover.
    )
    ok_button.place(x=50, y=110)  # Position the "OK" button.

    # Block: Add "Cancel" Button
    # Button to cancel the exit action and close the confirmation window.
    cancel_button = ctk.CTkButton(
        exit_screen,
        text='Cancel',  # Button text.
        bg_color='#8C6846',  # Background color.
        command=cancel_button,  # Function to call on click.
        width=30,  # Button width.
        height=30,  # Button height.
        font=('Cascadia Code', 14),  # Font style and size.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#9fa081'  # Color on hover.
    )
    cancel_button.place(x=150, y=110)  # Position the "Cancel" button.


# -------------------------------------------
# Function: delete_item
# Purpose:
# Deletes a selected book from the database after user confirmation.
# Refreshes the table to reflect the changes and handles potential errors.
# -------------------------------------------
def delete_item(main_root, tabla_information):
    # Block: Initialize Database Connection
    # Connects to the SQLite database and creates a cursor for executing queries.
    conn = sqlite3.connect('./db/bookstore_management.db')  # Connect to the database.
    cursor = conn.cursor()  # Create a cursor object.

    # Block: Retrieve Selected Item
    # Gets the currently selected item in the table.
    selected_item = tabla_information.selection()  # Get selected item.

    if selected_item:
        # Block: Extract Book ID
        # Retrieves the book ID from the selected item.
        book_id = tabla_information.item(selected_item[0])['values'][0]  # Extract book_id.

        # Block: Confirm Deletion
        # Asks the user to confirm the deletion of the selected book.
        message = messagebox.askyesno('Message', 'Do you want to delete this book?', parent=main_root)
        if message:
            try:
                # Block: Execute Deletion Query
                # Deletes the book from the database and reorders the remaining book IDs.
                cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))  # Delete the book.
                conn.commit()  # Commit the changes.

                # Block: Reorder Book IDs
                # Updates the book IDs to maintain a consecutive order after deletion.
                cursor.execute("""
                    WITH Ordered AS (
                        SELECT rowid, book_id, ROW_NUMBER() OVER (ORDER BY book_id) AS new_id
                        FROM books
                    )
                    UPDATE books
                    SET book_id = (SELECT new_id FROM Ordered WHERE Ordered.rowid = books.rowid)
                """)  # Reorder book IDs.
                conn.commit()  # Commit the changes.

                # Block: Refresh Table Display
                # Updates the table to reflect the deletion.
                refresh_table(tabla_information, cursor)  # Refresh the table.

                # Block: Inform User of Successful Deletion
                messagebox.showinfo('Message', 'Book deleted successfully!', parent=main_root)  # Success message.
            except Exception as e:
                # Block: Handle Deletion Errors
                # Displays an error message if the deletion fails.
                messagebox.showerror('Error', f"An error occurred: {e}", parent=main_root)  # Error message.
    else:
        # Block: No Selection Made
        # Informs the user that no item was selected for deletion.
        messagebox.showinfo('Message', "No item selected", parent=main_root)  # Informational message.

    # Block: Close Database Connection
    conn.close()  # Close the database connection.


# -------------------------------------------
# Function: refresh_table
# Purpose:
# Clears and repopulates the table with the latest data from the database.
# Ensures that the table display is up-to-date after any modifications.
# -------------------------------------------
def refresh_table(tabla_information, cursor):
    # Block: Clear Existing Table Entries
    # Removes all current entries from the table.
    for row in tabla_information.get_children():
        tabla_information.delete(row)  # Delete each row.

    # Block: Fetch Updated Data
    # Retrieves the latest book data from the database.
    cursor.execute("SELECT book_id, book_name, book_publisher, author_name, book_year, book_genre, book_language, book_ISBN, book_quantity FROM books ORDER BY book_id")  # Execute select query.
    for row in cursor.fetchall():
        tabla_information.insert("", "end", values=row)  # Insert each row into the table.


# -------------------------------------------
# Function: deselect_item
# Purpose:
# Deselects any selected item in the table if the user clicks outside of the table area.
# Enhances user experience by allowing easy deselection.
# -------------------------------------------
def deselect_item(event, tabla_information):
    # Block: Check Click Location
    # Determines if the click was outside the table and deselects items if so.
    if not tabla_information.winfo_containing(event.x_root, event.y_root) == tabla_information:
        tabla_information.selection_remove(tabla_information.selection())  # Deselect all items.


# -------------------------------------------
# Function: update_user_name_label
# Purpose:
# Updates the welcome label to display the username of the logged-in user.
# Defaults to "Guest" if no username is provided.
# -------------------------------------------
def update_user_name_label(name_label, username):
    if username:
        name_label.configure(text=f"Welcome, {username.upper()}")  # Display username in uppercase.
    else:
        name_label.configure(text="Welcome, Guest")  # Default to "Guest" if no username.
