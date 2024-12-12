import customtkinter as ctk  # CustomTkinter for modern GUI design with tkinter.
from PIL import Image  # PIL for image handling.
import sys  # Module to interact with the Python interpreter.
from tkinter import ttk  # Themed widgets for Tkinter.
from addBookWindow import add_book_window  # Function to open the "Add Book" window.
import tkinter.messagebox as messagebox  # Module for displaying message boxes.
import sqlite3  # SQLite3 for database management.
from functions import delete_item, deselect_item, update_user_name_label  # Custom utility functions.


# -------------------------------------------
# Function: main_window
# Purpose:
# Initializes and displays the main window of the bookstore management application.
# Sets up the user interface, including the treeview for displaying books,
# user information panel, search functionality, and action buttons.
# -------------------------------------------
def main_window():
    """
    Initializes and displays the main window of the bookstore management application.
    Sets up the user interface, including the treeview for displaying books,
    user information panel, search functionality, and action buttons.
    """

    # -------------------------------------------
    # Block: Initialize Main Application Window
    # Purpose:
    # Sets up the main window's properties such as size, title, icon, and theme.
    # -------------------------------------------
    main_root = ctk.CTk()  # Main application window instance.
    main_root.geometry('1400x800')  # Set window size.
    main_root.title('BooksTore')  # Set window title.
    main_root.resizable(True, True)  # Allow window resizing.
    ctk.set_default_color_theme('dark-blue')  # Set the default color theme.
    main_root.iconbitmap('./images/icobookstore.ico')  # Set window icon.

    # -------------------------------------------
    # Block: Center Main Window on Screen
    # Purpose:
    # Calculates and applies the position to center the window on the user's display.
    # -------------------------------------------
    screen_width = main_root.winfo_screenwidth()  # Retrieve screen width.
    screen_height = main_root.winfo_screenheight()  # Retrieve screen height.
    window_width = 1400  # Width of the main window.
    window_height = 800  # Height of the main window.
    pos_x = (screen_width // 2) - (window_width // 2)  # Calculate X position.
    pos_y = (screen_height // 2) - (window_height // 2)  # Calculate Y position.
    main_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')  # Apply position.

    # -------------------------------------------
    # Block: Configure Grid Layout
    # Purpose:
    # Sets up the grid layout to divide the main window into sections.
    # -------------------------------------------
    main_root.grid_rowconfigure(0, weight=1)  # Allow the first row to expand.
    main_root.grid_columnconfigure(1, weight=1)  # Allow the second column to expand.

    # -------------------------------------------
    # Block: Bind Events
    # Purpose:
    # Binds a left-click event to the main window to handle item deselection in the treeview.
    # -------------------------------------------
    main_root.bind("<Button-1>", lambda event: deselect_item(event, tabla_information))  # Bind left-click to deselect items.

    # -------------------------------------------
    # Block: Setup Treeview Frame
    # Purpose:
    # Creates a frame to hold the treeview widget and its scrollbars.
    # -------------------------------------------
    treeview_frame = ctk.CTkFrame(main_root)  # Frame for the treeview.
    treeview_frame.grid(row=0, column=1, sticky="nsew")  # Position the frame in the grid.

    # -------------------------------------------
    # Block: Initialize Scrollbars
    # Purpose:
    # Adds vertical and horizontal scrollbars to the treeview for navigation.
    # -------------------------------------------
    scrollbar_vertical = ctk.CTkScrollbar(treeview_frame, orientation="vertical")  # Vertical scrollbar.
    scrollbar_horizontal = ctk.CTkScrollbar(treeview_frame, orientation="horizontal")  # Horizontal scrollbar.

    # -------------------------------------------
    # Block: Define Hover Effects
    # Purpose:
    # Implements visual feedback when hovering over treeview rows.
    # -------------------------------------------
    def ttk_hover(event):
        """
        Highlights the row under the mouse cursor in the treeview.

        Parameters:
        - event: The event object containing information about the mouse movement.
        """
        my_line = tabla_information.identify_row(event.y)  # Identify the row under the cursor.

        if my_line:
            tabla_information.tag_configure('hover', background='#605b3e', foreground='#ffffff')  # Configure hover tag.

            for i in tabla_information.get_children():
                tabla_information.item(i, tags=('hover',) if i == my_line else ())  # Apply hover tag to the current row.

    def ttk_leave(event):
        """
        Removes the hover highlight from all rows in the treeview.

        Parameters:
        - event: The event object indicating the mouse has left the treeview.
        """
        for i in tabla_information.get_children():
            tabla_information.item(i, tags=())  # Remove all tags from rows.

    # -------------------------------------------
    # Block: Initialize Treeview
    # Purpose:
    # Creates the treeview widget to display book information with predefined columns.
    # -------------------------------------------
    tabla_information = ttk.Treeview(
        treeview_frame,
        columns=("book_id", "book_name", "book_publisher", "author_name", "book_year",
                 "book_genre", "book_language", "book_isbn", "book_quantity"),
        show='headings',
        yscrollcommand=scrollbar_vertical.set,
        xscrollcommand=scrollbar_horizontal.set
    )  # Treeview widget for displaying books.

    # -------------------------------------------
    # Block: Configure Treeview Style
    # Purpose:
    # Applies styling to the treeview for better aesthetics and usability.
    # -------------------------------------------
    style = ttk.Style()  # Initialize style.
    # Uncomment the next line to use a different theme.
    # style.theme_use('clam')  # Set a different theme if desired.
    style.configure("Treeview", rowheight=30, font=('Arial', 11))  # Configure row height and font.
    style.map(
        'Treeview',
        background=[('selected', '#4c2c18')],  # Background color when selected.
        foreground=[('selected', '#ffffff')],  # Foreground color when selected.
    )  # Map styles for selected rows.

    # -------------------------------------------
    # Block: Bind Hover Events to Treeview
    # Purpose:
    # Associates the hover and leave functions with the treeview events.
    # -------------------------------------------
    tabla_information.bind('<Motion>', ttk_hover)  # Bind mouse movement to hover effect.
    tabla_information.bind('<Leave>', ttk_leave)  # Bind mouse leave to remove hover effect.

    # -------------------------------------------
    # Block: Define Treeview Columns and Headings
    # Purpose:
    # Sets up the treeview columns with appropriate titles and properties.
    # -------------------------------------------
    # Setting column headers with appropriate titles.
    tabla_information.heading('book_id', text='Book ID')  # Column heading for Book ID.
    tabla_information.heading('book_name', text='Book Name')  # Column heading for Book Name.
    tabla_information.heading('book_publisher', text='Publisher')  # Column heading for Publisher.
    tabla_information.heading('author_name', text='Author Name')  # Column heading for Author Name.
    tabla_information.heading('book_year', text='Year')  # Column heading for Year.
    tabla_information.heading('book_genre', text='Genre')  # Column heading for Genre.
    tabla_information.heading('book_language', text='Language')  # Column heading for Language.
    tabla_information.heading('book_isbn', text='ISBN')  # Column heading for ISBN.
    tabla_information.heading('book_quantity', text='Quantity')  # Column heading for Quantity.

    # Define the columns and set their properties: width, alignment, and labels.
    columns = (
        "book_id", "book_name", "book_publisher", "author_name", "book_year",
        "book_genre", "book_language", "book_isbn", "book_quantity"
    )  # List of column identifiers.

    for column in columns:
        if column in ("book_name", "book_publisher", "author_name"):
            tabla_information.column(column, width=250, anchor='w', stretch=False)  # Wide columns for text.
        elif column == "book_id":
            tabla_information.column(column, width=50, anchor='center', stretch=False)  # Narrow column for ID.
        else:
            tabla_information.column(column, width=250, anchor='center', stretch=False)  # Other columns.

    # -------------------------------------------
    # Block: Pack Scrollbars and Treeview
    # Purpose:
    # Adds the scrollbars and treeview to the frame, enabling navigation through the book records.
    # -------------------------------------------
    scrollbar_vertical.configure(command=tabla_information.yview)  # Configure vertical scrollbar.
    scrollbar_horizontal.configure(command=tabla_information.xview)  # Configure horizontal scrollbar.
    scrollbar_vertical.pack(side='left', fill='y')  # Pack vertical scrollbar to the left.
    scrollbar_horizontal.pack(side='bottom', fill='x')  # Pack horizontal scrollbar to the bottom.
    tabla_information.pack(side='left', fill='both', expand=True)  # Pack treeview to fill the remaining space.

    # -------------------------------------------
    # Block: Setup Left Panel
    # Purpose:
    # Creates a left-side panel containing user information, search filters, and action buttons.
    # -------------------------------------------
    left_frame = ctk.CTkFrame(main_root, width=300, height=800, corner_radius=10)  # Left panel frame.
    left_frame.grid(row=0, column=0, sticky="ns")  # Position the left panel in the grid.
    left_frame.grid_propagate(False)  # Prevent frame from resizing based on its content.

    # -------------------------------------------
    # Block: Add Footer to Left Panel
    # Purpose:
    # Adds a footer at the bottom of the left panel with fixed text.
    # -------------------------------------------
    left_frame.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand.
    foot_frame = ctk.CTkFrame(left_frame, fg_color="#4c2c18", height=30)  # Footer frame.
    foot_frame.grid(row=2, column=0, sticky="nsew")  # Position the footer in the grid.
    left_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand.
    foot_frame_label = ctk.CTkLabel(
        foot_frame,
        text=' Ivy Tech Community College 2024',  # Footer text.
        font=("Cascadia Code", 14),
        text_color='White'
    )
    foot_frame_label.pack(expand=True, pady=5)  # Center the footer label.

    # -------------------------------------------
    # Block: Add User Avatar
    # Purpose:
    # Displays a user image or a placeholder text in the left panel.
    # -------------------------------------------
    try:
        p_imagen = Image.open('./images/userbook.png')  # Open user image.
        r_imagen = ctk.CTkImage(p_imagen, size=(70, 70))  # Resize image.
        user_label_imagen = ctk.CTkLabel(left_frame, image=r_imagen, text="")  # Label for user image.
    except Exception:
        user_label_imagen = ctk.CTkLabel(left_frame, text="Not Found", font=("Cascadia Code", 14, "bold"))  # Placeholder text if image not found.

    user_label_imagen.place(x=120, y=50)  # Position the user avatar.

    # -------------------------------------------
    # Block: Add Welcome Label
    # Purpose:
    # Displays the username of the logged-in user or "Guest" if no username is provided.
    # -------------------------------------------
    name_label = ctk.CTkLabel(left_frame, text="User Name", font=('Cascadia Code', 12))  # Welcome label.
    name_label.place(x=105, y=130)  # Position the welcome label.
    username = sys.argv[1] if len(sys.argv) > 1 else None  # Retrieve username from command-line arguments.
    update_user_name_label(name_label, username)  # Update the welcome label with the username.

    # -------------------------------------------
    # Block: Add Search Filters
    # Purpose:
    # Provides dropdowns and entry fields for users to search and filter book records.
    # -------------------------------------------
    search_filter = ctk.CTkComboBox(
        left_frame,
        values=['Book Name', 'Language', 'ISBN', 'Author Name', 'Publisher', 'Year'],
        width=200,
        height=30,
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12)
    )  # Dropdown for selecting search criteria.
    search_filter.set('')  # Set default value.
    search_filter.place(x=60, y=200)  # Position the search filter dropdown.

    search_entry = ctk.CTkEntry(left_frame, placeholder_text=' Type information')  # Entry for search input.
    search_entry.place(x=60, y=270)  # Position the search entry field.

    # -------------------------------------------
    # Block: Add Clear Search Button
    # Purpose:
    # Adds a button to clear the search filters and input fields.
    # -------------------------------------------
    def clear_command():
        """
        Clears the search filter selections and input fields.
        """
        search_filter.set('')  # Reset search filter dropdown.
        search_entry.delete(0, 'end')  # Clear search entry field.

    search_button_clear = ctk.CTkButton(
        left_frame,
        text='Clear',  # Button text.
        width=25,  # Button width.
        height=28,  # Button height.
        command=clear_command,  # Function to call on click.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14)  # Font style and size.
    )
    search_button_clear.place(x=203, y=270)  # Position the "Clear" button.

    # -------------------------------------------
    # Block: Define Button Dimensions and Positions
    # Purpose:
    # Sets consistent dimensions and calculates positions for action buttons.
    # -------------------------------------------
    button_width = 190  # Width for action buttons.
    button_x = (300 - button_width) // 2  # Calculate X position to center buttons.

    # -------------------------------------------
    # Block: Add Action Buttons
    # Purpose:
    # Adds buttons for adding, editing, deleting, viewing, and renting books.
    # -------------------------------------------
    # Add Book Button
    add_book_button = ctk.CTkButton(
        left_frame,
        text='Add Book',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=200,  # Button width.
        height=30,  # Button height.
        command=lambda: add_book_window(main_root, tabla_information, refresh_treeview)  # Open "Add Book" window.
    )
    add_book_button.place(x=button_x, y=340)  # Position the "Add Book" button.

    # Edit Book Button
    edit_book_button = ctk.CTkButton(
        left_frame,
        text='Edit Book',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=200,  # Button width.
        height=30,  # Button height.
        command=lambda: messagebox.showinfo(
            'Maintenance',
            "Work is being done on this page",
            parent=main_root
        )  # Placeholder action for editing books.
    )
    edit_book_button.place(x=button_x, y=410)  # Position the "Edit Book" button.

    # Delete Book Button
    delete_book_button = ctk.CTkButton(
        left_frame,
        text='Delete Book',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=200,  # Button width.
        height=30,  # Button height.
        command=lambda: delete_item(main_root, tabla_information)  # Call delete_item function.
    )
    delete_book_button.place(x=button_x, y=480)  # Position the "Delete Book" button.

    # Book Information Button
    info_book_button = ctk.CTkButton(
        left_frame,
        text='Book Information',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=200,  # Button width.
        height=30,  # Button height.
        command=lambda: messagebox.showinfo(
            'Maintenance',
            "Work is being done on this page",
            parent=main_root
        )  # Placeholder action for book information.
    )
    info_book_button.place(x=button_x, y=550)  # Position the "Book Information" button.

    # Rent Book Button
    rent_book_button = ctk.CTkButton(
        left_frame,
        text='Rent Book',  # Button text.
        fg_color='#605b3e',  # Foreground color.
        hover_color='#4c2c18',  # Hover color.
        font=('Cascadia Code', 14),  # Font style and size.
        width=200,  # Button width.
        height=30,  # Button height.
        command=lambda: messagebox.showinfo(
            'Maintenance',
            "Work is being done on this page",
            parent=main_root
        )  # Placeholder action for renting books.
    )
    rent_book_button.place(x=button_x, y=620)  # Position the "Rent Book" button.

    # -------------------------------------------
    # Block: Populate Treeview with Book Records
    # Purpose:
    # Fetches and displays existing book records from the database in the treeview.
    # -------------------------------------------
    def populate_treeview():
        """
        Connects to the SQLite database, retrieves all book records, and inserts them into the treeview.
        """
        try:
            connection = sqlite3.connect('./db/bookstore_management.db')  # Connect to the database.
            cursor = connection.cursor()  # Create a cursor object.
            query = """
            SELECT book_id, book_name, book_publisher, author_name, 
                   book_year, book_genre, book_language, book_ISBN, book_quantity 
            FROM books;
            """  # SQL query to select all book records.
            cursor.execute(query)  # Execute the query.
            rows = cursor.fetchall()  # Fetch all results.

            for row in rows:
                tabla_information.insert("", "end", values=row)  # Insert each row into the treeview.

            cursor.close()  # Close the cursor.
            connection.close()  # Close the database connection.
        except sqlite3.Error as err:
            print(f"Error: {err}")  # Print any database errors.

    populate_treeview()  # Populate the treeview upon initialization.

    # -------------------------------------------
    # Block: Define Refresh Treeview Function
    # Purpose:
    # Refreshes the treeview by clearing existing entries and fetching updated data from the database.
    # -------------------------------------------
    def refresh_treeview(tabla_information):
        """
        Refreshes the treeview by clearing existing entries and fetching updated data from the database.

        Parameters:
        - tabla_information: The treeview widget to be refreshed.
        """
        for item in tabla_information.get_children():
            tabla_information.delete(item)  # Remove all existing entries.

        try:
            conn = sqlite3.connect('./db/bookstore_management.db')  # Connect to the database.
            cursor = conn.cursor()  # Create a cursor object.
            cursor.execute(
                'SELECT book_id, book_name, book_publisher, author_name, book_year, book_genre, book_language, book_ISBN, book_quantity FROM books'
            )  # SQL query to select all book records.
            rows = cursor.fetchall()  # Fetch all results.

            for row in rows:
                tabla_information.insert("", "end", values=row)  # Insert each row into the treeview.

            conn.close()  # Close the database connection.
        except sqlite3.Error as err:
            print(f"Error refreshing treeview: {err}")  # Print any database errors.

    # -------------------------------------------
    # Block: Start Main Event Loop
    # Purpose:
    # Initiates the Tkinter event loop to display and manage the main application window.
    # -------------------------------------------
    main_root.mainloop()  # Start the Tkinter event loop.


# -------------------------------------------
# Execution: Start Main Window
# Purpose:
# Calls the main_window function to launch the bookstore management application.
# -------------------------------------------
if __name__ == "__main__":
    main_window()  # Execute the main window function to start the application.
