import customtkinter as ctk
import tkinter.messagebox as messagebox
import sqlite3


# Function to create a new window for adding books
def add_book_window(main_root, tabla_information, refresh_treeview):
    """
    Creates and manages the "Add Book" window, allowing users to input and submit new book details.

    Parameters:
    - main_root: The main application window.
    - tabla_information: The treeview or table widget displaying book information.
    - refresh_treeview: A callback function to refresh the treeview after adding a new book.
    """

    # Initialize the "Add Book" window as a Toplevel window with specific properties
    add_book_root = ctk.CTkToplevel(main_root)
    add_book_root.geometry('400x600')
    ctk.set_default_color_theme('dark-blue')  # Set the default color theme
    add_book_root.resizable(False, False)
    add_book_root.after(200, lambda: add_book_root.iconbitmap('./images/icobookstore.ico'))  # Set window icon
    add_book_root.title('BooksTore')

    # Center the "Add Book" window on the user's screen
    screen_width = add_book_root.winfo_screenwidth()
    screen_height = add_book_root.winfo_screenheight()
    window_width = 400
    window_height = 600
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    add_book_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    # Make the "Add Book" window modal to prevent interaction with the main window
    add_book_root.transient(main_root)
    add_book_root.grab_set()
    add_book_root.lift()
    add_book_root.attributes('-topmost', True)

    # Create labels and entry fields for book information
    # Book Name
    bookname_label = ctk.CTkLabel(add_book_root, text='Book Name:', font=('Cascadia Code', 14))
    bookname_label.place(x=30, y=50)
    bookname_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    bookname_entry.place(x=185, y=50)

    # Publisher Name
    publisher_label = ctk.CTkLabel(add_book_root, text='Publisher Name:', font=('Cascadia Code', 14))
    publisher_label.place(x=30, y=100)
    publisher_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    publisher_entry.place(x=185, y=100)

    # Author Name
    author_label = ctk.CTkLabel(add_book_root, text='Author Name:', font=('Cascadia Code', 14))
    author_label.place(x=30, y=145)
    author_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    author_entry.place(x=185, y=145)

    # Book Year
    book_year_label = ctk.CTkLabel(add_book_root, text='Book Year:', font=('Cascadia Code', 14))
    book_year_label.place(x=30, y=190)
    book_year_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    book_year_entry.place(x=185, y=190)

    # Genre Selection
    genre_label = ctk.CTkLabel(add_book_root, text='Genre:', font=('Cascadia Code', 14))
    genre_label.place(x=30, y=235)
    genre_cbx = ctk.CTkComboBox(
        add_book_root,
        values=['Fantasy', 'Science fiction', 'Horror', 'Romance', 'Historical fiction', 'Drama', 'Other'],
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12),
        width=190
    )
    genre_cbx.set('')
    genre_cbx.place(x=185, y=235)

    # Language Selection
    category_label = ctk.CTkLabel(add_book_root, text='Language:', font=('Cascadia Code', 14))
    category_label.place(x=30, y=280)
    category_cbx = ctk.CTkComboBox(
        add_book_root,
        values=['Fiction', 'EN', 'ES', 'RU', 'IT', 'HI', 'HI', 'AR', 'PT', 'JA', 'CM', 'FR', 'Other'],
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12),
        width=190
    )
    category_cbx.set('')
    category_cbx.place(x=185, y=280)

    # ISBN Entry
    isbn_label = ctk.CTkLabel(add_book_root, text='Book ISBN:', font=('Cascadia Code', 14))
    isbn_label.place(x=30, y=325)
    isbn_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    isbn_entry.place(x=185, y=325)

    # Quantity Entry
    quantity_label = ctk.CTkLabel(add_book_root, text='Book Quantity:', font=('Cascadia Code', 14))
    quantity_label.place(x=30, y=370)
    quantity_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    quantity_entry.place(x=185, y=370)

    # Define genre and language options for validation
    GENRE_VALUES = ['Fiction', 'Fantasy', 'Science fiction', 'Horror', 'Romance', 'Historical fiction', 'Drama',
                    'Other']
    LANGUAGE_VALUES = ['EN', 'ES', 'RU', 'IT', 'HI', 'HI', 'AR', 'PT', 'JA', 'CM', 'FR', 'Other']

    # Function to clear all input fields
    def clear_info():
        """
        Clears all the input fields in the "Add Book" window.
        """
        bookname_entry.delete(0, 'end')
        publisher_entry.delete(0, 'end')
        author_entry.delete(0, 'end')
        book_year_entry.delete(0, 'end')
        genre_cbx.set('')
        category_cbx.set('')
        isbn_entry.delete(0, 'end')
        quantity_entry.delete(0, 'end')

    # Function to retrieve the next available book ID from the database
    def get_next_book_id():
        """
        Retrieves the next available book ID by finding the maximum existing ID and incrementing it.

        Returns:
        - next_book_id (int): The next available book ID.
        """
        conn = sqlite3.connect('./db/bookstore_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(book_id) FROM books')
        max_id = cursor.fetchone()[0]
        conn.close()
        return max_id + 1 if max_id else 1

    # Function to validate the selected ComboBox values
    def validate_combobox_values(genre, language):
        """
        Validates the selected genre and language against predefined lists.

        Parameters:
        - genre (str): The selected genre.
        - language (str): The selected language.

        Returns:
        - bool: True if both selections are valid, False otherwise.
        """
        if genre not in GENRE_VALUES:
            messagebox.showerror('Invalid Input', f"Invalid Genre: '{genre}'. Please select a valid option.",
                                 parent=add_book_root)
            return False
        if language not in LANGUAGE_VALUES:
            messagebox.showerror('Invalid Input', f"Invalid Language: '{language}'. Please select a valid option.",
                                 parent=add_book_root)
            return False
        return True

    # Function to submit the book information to the database
    def submit_book_info():
        """
        Gathers input data, validates it, inserts the new book into the database,
        refreshes the treeview, and provides user feedback.
        """
        # Retrieve data from input fields
        book_name = bookname_entry.get()
        publisher_name = publisher_entry.get()
        author_name = author_entry.get()
        book_year = book_year_entry.get()
        genre = genre_cbx.get()
        language = category_cbx.get()
        isbn = isbn_entry.get()
        quantity = quantity_entry.get()

        # Ensure all fields are filled
        if not all([book_name, publisher_name, author_name, book_year, genre, language, isbn, quantity]):
            messagebox.showerror('Error', 'All fields are required!', parent=add_book_root)
            return

        # Validate ComboBox selections
        if not validate_combobox_values(genre, language):
            return

        # Get the next available book ID
        next_book_id = get_next_book_id()

        # Connect to the SQLite database and insert the new book record
        conn = sqlite3.connect('./db/bookstore_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (book_id, book_name, book_publisher, author_name, book_year, book_genre, book_language, book_ISBN, book_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (next_book_id, book_name, publisher_name, author_name, book_year, genre, language, isbn, quantity))
        conn.commit()
        conn.close()

        # Inform the user of the successful addition
        messagebox.showinfo('Message', 'Book information added successfully!', parent=add_book_root)

        # Refresh the treeview to display the new book
        refresh_treeview(tabla_information)

        # Clear the input fields for new entries
        clear_info()

    # Create the "Submit" button to save the book information
    submit_button = ctk.CTkButton(
        add_book_root,
        text='Submit',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=150,
        height=30,
        command=submit_book_info  # Directly call the submit function
    )
    submit_button.place(x=30, y=500)

    # Create the "Clear" button to reset all input fields
    clear_button = ctk.CTkButton(
        add_book_root,
        text='Clear',
        fg_color='#605b3e',
        command=clear_info,
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=150,
        height=30
    )
    clear_button.place(x=215, y=500)

    # Run the "Add Book" window's event loop
    add_book_root.mainloop()
