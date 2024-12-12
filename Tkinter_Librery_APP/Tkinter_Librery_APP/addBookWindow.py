import customtkinter as ctk  # CustomTkinter for modern GUI design with tkinter.
import tkinter.messagebox as messagebox  # Module for displaying message boxes.
import sqlite3  # SQLite3 for database management.

# -------------------------------------------
# Function: add_book_window
# Purpose:
# Creates and manages the "Add Book" window, allowing users to input and submit new book details.
# -------------------------------------------
def add_book_window(main_root, tabla_information, refresh_treeview):
    """
    Creates and manages the "Add Book" window, allowing users to input and submit new book details.

    Parameters:
    - main_root: The main application window.
    - tabla_information: The treeview or table widget displaying book information.
    - refresh_treeview: A callback function to refresh the treeview after adding a new book.
    """

    # -------------------------------------------
    # Block: Initialize "Add Book" Window
    # Purpose:
    # Sets up the "Add Book" window with specified size, appearance, and modality.
    # -------------------------------------------
    add_book_root = ctk.CTkToplevel(main_root)  # "Add Book" window instance.
    add_book_root.geometry('400x600')  # Set window size.
    ctk.set_default_color_theme('dark-blue')  # Set the default color theme.
    add_book_root.resizable(False, False)  # Disable window resizing.
    add_book_root.after(200, lambda: add_book_root.iconbitmap('./images/icobookstore.ico'))  # Set window icon after 200ms.
    add_book_root.title('BooksTore')  # Set window title.

    # -------------------------------------------
    # Block: Center "Add Book" Window on Screen
    # Purpose:
    # Calculates and applies the position to center the window on the user's display.
    # -------------------------------------------
    screen_width = add_book_root.winfo_screenwidth()  # Retrieve screen width.
    screen_height = add_book_root.winfo_screenheight()  # Retrieve screen height.
    window_width = 400  # Width of the "Add Book" window.
    window_height = 600  # Height of the "Add Book" window.
    pos_x = (screen_width // 2) - (window_width // 2)  # Calculate X position.
    pos_y = (screen_height // 2) - (window_height // 2)  # Calculate Y position.
    add_book_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')  # Apply position.

    # -------------------------------------------
    # Block: Make "Add Book" Window Modal
    # Purpose:
    # Ensures that the "Add Book" window is modal, preventing interaction with the main window.
    # -------------------------------------------
    add_book_root.transient(main_root)  # Set as transient window.
    add_book_root.grab_set()  # Grab all events.
    add_book_root.lift()  # Bring to front.
    add_book_root.attributes('-topmost', True)  # Keep on top.

    # -------------------------------------------
    # Block: Create Labels and Entry Fields for Book Information
    # Purpose:
    # Sets up the input fields for various book attributes such as name, publisher, author, etc.
    # -------------------------------------------
    # Book Name
    bookname_label = ctk.CTkLabel(add_book_root, text='Book Name:', font=('Cascadia Code', 14))  # Label for Book Name.
    bookname_label.place(x=30, y=50)  # Position the label.
    bookname_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)  # Entry for Book Name.
    bookname_entry.place(x=185, y=50)  # Position the entry field.

    # Publisher Name
    publisher_label = ctk.CTkLabel(add_book_root, text='Publisher Name:', font=('Cascadia Code', 14))  # Label for Publisher Name.
    publisher_label.place(x=30, y=100)  # Position the label.
    publisher_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)  # Entry for Publisher Name.
    publisher_entry.place(x=185, y=100)  # Position the entry field.

    # Author Name
    author_label = ctk.CTkLabel(add_book_root, text='Author Name:', font=('Cascadia Code', 14))  # Label for Author Name.
    author_label.place(x=30, y=145)  # Position the label.
    author_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)  # Entry for Author Name.
    author_entry.place(x=185, y=145)  # Position the entry field.

    # Book Year
    book_year_label = ctk.CTkLabel(add_book_root, text='Book Year:', font=('Cascadia Code', 14))  # Label for Book Year.
    book_year_label.place(x=30, y=190)  # Position the label.
    book_year_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)  # Entry for Book Year.
    book_year_entry.place(x=185, y=190)  # Position the entry field.

    # Genre Selection
    genre_label = ctk.CTkLabel(add_book_root, text='Genre:', font=('Cascadia Code', 14))  # Label for Genre.
    genre_label.place(x=30, y=235)  # Position the label.
    genre_cbx = ctk.CTkComboBox(
        add_book_root,
        values=['Fantasy', 'Science fiction', 'Horror', 'Romance', 'Historical fiction', 'Drama', 'Other'],
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12),
        width=190
    )  # ComboBox for Genre selection.
    genre_cbx.set('')  # Set default value.
    genre_cbx.place(x=185, y=235)  # Position the ComboBox.

    # Language Selection
    category_label = ctk.CTkLabel(add_book_root, text='Language:', font=('Cascadia Code', 14))  # Label for Language.
    category_label.place(x=30, y=280)  # Position the label.
    category_cbx = ctk.CTkComboBox(
        add_book_root,
        values=['Fiction', 'EN', 'ES', 'RU', 'IT', 'HI', 'HI', 'AR', 'PT', 'JA', 'CM', 'FR', 'Other'],
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12),
        width=190
    )  # ComboBox for Language selection.
    category_cbx.set('')  # Set default value.
    category_cbx.place(x=185, y=280)  # Position the ComboBox.

    # ISBN Entry
    isbn_label = ctk.CTkLabel(add_book_root, text='Book ISBN:', font=('Cascadia Code', 14))  # Label for ISBN.
    isbn_label.place(x=30, y=325)  # Position the label.
    isbn_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)  # Entry for ISBN.
    isbn_entry.place(x=185, y=325)  # Position the entry field.

    # Quantity Entry
    quantity_label = ctk.CTkLabel(add_book_root, text='Book Quantity:', font=('Cascadia Code', 14))  # Label for Quantity.
    quantity_label.place(x=30, y=370)  # Position the label.
    quantity_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)  # Entry for Quantity.
    quantity_entry.place(x=185, y=370)  # Position the entry field.

    # -------------------------------------------
    # Block: Define Genre and Language Options for Validation
    # Purpose:
    # Sets predefined valid options for genre and language to ensure data integrity.
    # -------------------------------------------
    GENRE_VALUES = ['Fiction', 'Fantasy', 'Science fiction', 'Horror', 'Romance', 'Historical fiction', 'Drama', 'Other']  # Valid genres.
    LANGUAGE_VALUES = ['EN', 'ES', 'RU', 'IT', 'HI', 'HI', 'AR', 'PT', 'JA', 'CM', 'FR', 'Other']  # Valid languages.

    # -------------------------------------------
    # Block: Define Helper Functions
    # Purpose:
    # Includes functions to clear input fields, retrieve the next book ID, validate selections, and submit book information.
    # -------------------------------------------
    # Function: clear_info
    # Purpose:
    # Clears all the input fields in the "Add Book" window.
    def clear_info():
        bookname_entry.delete(0, 'end')  # Clear Book Name.
        publisher_entry.delete(0, 'end')  # Clear Publisher Name.
        author_entry.delete(0, 'end')  # Clear Author Name.
        book_year_entry.delete(0, 'end')  # Clear Book Year.
        genre_cbx.set('')  # Reset Genre selection.
        category_cbx.set('')  # Reset Language selection.
        isbn_entry.delete(0, 'end')  # Clear ISBN.
        quantity_entry.delete(0, 'end')  # Clear Quantity.

    # Function: get_next_book_id
    # Purpose:
    # Retrieves the next available book ID by finding the maximum existing ID and incrementing it.
    def get_next_book_id():
        conn = sqlite3.connect('./db/bookstore_management.db')  # Connect to the database.
        cursor = conn.cursor()  # Create a cursor object.
        cursor.execute('SELECT MAX(book_id) FROM books')  # Query to find the maximum book ID.
        max_id = cursor.fetchone()[0]  # Fetch the result.
        conn.close()  # Close the database connection.
        return max_id + 1 if max_id else 1  # Return the next book ID.

    # Function: validate_combobox_values
    # Purpose:
    # Validates the selected genre and language against predefined lists.
    def validate_combobox_values(genre, language):
        if genre not in GENRE_VALUES:
            messagebox.showerror('Invalid Input', f"Invalid Genre: '{genre}'. Please select a valid option.", parent=add_book_root)  # Show error for invalid genre.
            return False
        if language not in LANGUAGE_VALUES:
            messagebox.showerror('Invalid Input', f"Invalid Language: '{language}'. Please select a valid option.", parent=add_book_root)  # Show error for invalid language.
            return False
        return True  # Valid selections.

    # Function: submit_book_info
    # Purpose:
    # Gathers input data, validates it, inserts the new book into the database,
    # refreshes the treeview, and provides user feedback.
    def submit_book_info():
        # Retrieve data from input fields.
        book_name = bookname_entry.get()
        publisher_name = publisher_entry.get()
        author_name = author_entry.get()
        book_year = book_year_entry.get()
        genre = genre_cbx.get()
        language = category_cbx.get()
        isbn = isbn_entry.get()
        quantity = quantity_entry.get()

        # Ensure all fields are filled.
        if not all([book_name, publisher_name, author_name, book_year, genre, language, isbn, quantity]):
            messagebox.showerror('Error', 'All fields are required!', parent=add_book_root)  # Show error if any field is empty.
            return

        # Validate ComboBox selections.
        if not validate_combobox_values(genre, language):
            return  # Exit if validation fails.

        # Get the next available book ID.
        next_book_id = get_next_book_id()

        # Connect to the SQLite database and insert the new book record.
        conn = sqlite3.connect('./db/bookstore_management.db')  # Connect to the database.
        cursor = conn.cursor()  # Create a cursor object.
        cursor.execute('''
            INSERT INTO books (book_id, book_name, book_publisher, author_name, book_year, book_genre, book_language, book_ISBN, book_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (next_book_id, book_name, publisher_name, author_name, book_year, genre, language, isbn, quantity))  # Insert new book.
        conn.commit()  # Commit the transaction.
        conn.close()  # Close the database connection.

        # Inform the user of the successful addition.
        messagebox.showinfo('Message', 'Book information added successfully!', parent=add_book_root)  # Success message.

        # Refresh the treeview to display the new book.
        refresh_treeview(tabla_information)  # Refresh the treeview.

        # Clear the input fields for new entries.
        clear_info()  # Clear all input fields.

    # -------------------------------------------
    # Block: Create Action Buttons
    # Purpose:
    # Adds "Submit" and "Clear" buttons to handle form submission and resetting inputs.
    # -------------------------------------------
    # Submit Button
    submit_button = ctk.CTkButton(
        add_book_root,
        text='Submit',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=150,  # Button width.
        height=30,  # Button height.
        command=submit_book_info  # Function to call on click.
    )
    submit_button.place(x=30, y=500)  # Position the "Submit" button.

    # Clear Button
    clear_button = ctk.CTkButton(
        add_book_root,
        text='Clear',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        command=clear_info,  # Function to call on click.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=150,  # Button width.
        height=30  # Button height.
    )
    clear_button.place(x=215, y=500)  # Position the "Clear" button.

    # -------------------------------------------
    # Block: Run "Add Book" Window's Event Loop
    # Purpose:
    # Initiates the Tkinter event loop to display and manage the "Add Book" window.
    # -------------------------------------------
    add_book_root.mainloop()  # Start the Tkinter event loop.

