import customtkinter as ctk
from PIL import Image
import sys
from tkinter import ttk

from addBookWindow import add_book_window
import tkinter.messagebox as messagebox
import sqlite3
from functions import delete_item, deselect_item, update_user_name_label


# Main function to initialize and display the bookstore management window.
def main_window():
    """
    Initializes and displays the main window of the bookstore management application.
    Sets up the user interface, including the treeview for displaying books,
    user information panel, search functionality, and action buttons.
    """

    # Initialize the main application window with specific properties.
    main_root = ctk.CTk()
    main_root.geometry('1400x800')
    main_root.title('BooksTore')
    main_root.resizable(True, True)
    ctk.set_default_color_theme('dark-blue')  # Set the default color theme
    main_root.iconbitmap('./images/icobookstore.ico')  # Set window icon

    # Center the main window on the user's screen.
    screen_width = main_root.winfo_screenwidth()
    screen_height = main_root.winfo_screenheight()
    window_width = 1400
    window_height = 800
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    main_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    # Configure the grid layout to split the window into two sections.
    main_root.grid_rowconfigure(0, weight=1)
    main_root.grid_columnconfigure(1, weight=1)

    # Bind a left-click event to deselect items in the treeview.
    main_root.bind("<Button-1>", lambda event: deselect_item(event, tabla_information))

    # Frame for displaying the table with book records.
    # Contains a Treeview widget and scrollbars.
    treeview_frame = ctk.CTkFrame(main_root)
    treeview_frame.grid(row=0, column=1, sticky="nsew")

    # Initialize vertical and horizontal scrollbars for the treeview.
    scrollbar_vertical = ctk.CTkScrollbar(treeview_frame, orientation="vertical")
    scrollbar_horizontal = ctk.CTkScrollbar(treeview_frame, orientation="horizontal")

    # Function to handle row hover effects in the treeview.
    def ttk_hover(event):
        """
        Highlights the row under the mouse cursor in the treeview.

        Parameters:
        - event: The event object containing information about the mouse movement.
        """
        my_line = tabla_information.identify_row(event.y)

        if my_line:
            tabla_information.tag_configure('hover', background='#605b3e', foreground='#ffffff')

            for i in tabla_information.get_children():
                tabla_information.item(i, tags=('hover',) if i == my_line else ())

    # Function to remove hover effects when the mouse leaves the treeview.
    def ttk_leave(event):
        """
        Removes the hover highlight from all rows in the treeview.

        Parameters:
        - event: The event object indicating the mouse has left the treeview.
        """
        for i in tabla_information.get_children():
            tabla_information.item(i, tags=())

    # Treeview widget to display book information with predefined columns.
    tabla_information = ttk.Treeview(
        treeview_frame,
        columns=("book_id", "book_name", "book_publisher", "author_name", "book_year",
                 "book_genre", "book_language", "book_isbn", "book_quantity"),
        show='headings',
        yscrollcommand=scrollbar_vertical.set,
        xscrollcommand=scrollbar_horizontal.set
    )

    # Configure the style of the treeview for better aesthetics.
    style = ttk.Style()
    # Uncomment the next line to use a different theme.
    # style.theme_use('clam')
    style.configure("Treeview", rowheight=30, font=('Arial', 11))
    style.map(
        'Treeview',
        background=[('selected', '#4c2c18')],
        foreground=[('selected', '#ffffff')],
    )

    # Bind hover and leave events to the treeview for interactive effects.
    tabla_information.bind('<Motion>', ttk_hover)
    tabla_information.bind('<Leave>', ttk_leave)

    # Setting column headers with appropriate titles.
    tabla_information.heading('book_id', text='Book ID')
    tabla_information.heading('book_name', text='Book Name')
    tabla_information.heading('book_publisher', text='Publisher')
    tabla_information.heading('author_name', text='Author Name')
    tabla_information.heading('book_year', text='Year')
    tabla_information.heading('book_genre', text='Genre')
    tabla_information.heading('book_language', text='Language')
    tabla_information.heading('book_isbn', text='ISBN')
    tabla_information.heading('book_quantity', text='Quantity')

    # Define the columns and set their properties: width, alignment, and labels.
    columns = (
        "book_id", "book_name", "book_publisher", "author_name", "book_year",
        "book_genre", "book_language", "book_isbn", "book_quantity"
    )

    for column in columns:
        if column in ("book_name", "book_publisher", "author_name"):
            tabla_information.column(column, width=250, anchor='w', stretch=False)
        elif column == "book_id":
            tabla_information.column(column, width=50, anchor='center', stretch=False)
        else:
            tabla_information.column(column, width=250, anchor='center', stretch=False)

    # Pack the scrollbars and treeview into the frame.
    scrollbar_vertical.configure(command=tabla_information.yview)
    scrollbar_horizontal.configure(command=tabla_information.xview)
    scrollbar_vertical.pack(side='left', fill='y')
    scrollbar_horizontal.pack(side='bottom', fill='x')
    tabla_information.pack(side='left', fill='both', expand=True)

    # Left panel: contains user info, search filters, and action buttons.
    left_frame = ctk.CTkFrame(main_root, width=300, height=800, corner_radius=10)
    left_frame.grid(row=0, column=0, sticky="ns")
    left_frame.grid_propagate(False)

    # Footer at the bottom of the left panel with fixed text.
    left_frame.grid_rowconfigure(1, weight=1)
    foot_frame = ctk.CTkFrame(left_frame, fg_color="#4c2c18", height=30)
    foot_frame.grid(row=2, column=0, sticky="nsew")
    left_frame.grid_columnconfigure(0, weight=1)
    foot_frame_label = ctk.CTkLabel(
        foot_frame,
        text=' Ivy Tech Community College 2024',
        font=("Cascadia Code", 14),
        text_color='White'
    )
    foot_frame_label.pack(expand=True, pady=5)

    # User avatar: displays a user image or a placeholder text.
    try:
        p_imagen = Image.open('./images/userbook.png')
        r_imagen = ctk.CTkImage(p_imagen, size=(70, 70))
        user_label_imagen = ctk.CTkLabel(left_frame, image=r_imagen, text="")
    except Exception:
        user_label_imagen = ctk.CTkLabel(left_frame, text="Not Found", font=("Cascadia Code", 14, "bold"))

    user_label_imagen.place(x=120, y=50)

    # 'Welcome' label displaying the username or "Guest".
    name_label = ctk.CTkLabel(left_frame, text="User Name", font=('Cascadia Code', 12))
    name_label.place(x=105, y=130)
    username = sys.argv[1] if len(sys.argv) > 1 else None
    update_user_name_label(name_label, username)

    # Search filter dropdown and text entry for filtering book records.
    search_filter = ctk.CTkComboBox(
        left_frame,
        values=['Book Name', 'Language', 'ISBN', 'Author Name', 'Publisher', 'Year'],
        width=200,
        height=30,
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12)
    )
    search_filter.set('')
    search_filter.place(x=60, y=200)

    search_entry = ctk.CTkEntry(left_frame, placeholder_text=' Type information')
    search_entry.place(x=60, y=270)

    # Function to clear search filters.
    def clear_command():
        """
        Clears the search filter selections and input fields.
        """
        search_filter.set('')
        search_entry.delete(0, 'end')

    # Button to clear search filters.
    search_button_clear = ctk.CTkButton(
        left_frame,
        text='Clear',
        width=25,
        height=28,
        command=clear_command,
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14)
    )
    search_button_clear.place(x=203, y=270)

    # Define button dimensions and positions for consistency.
    button_width = 190
    button_x = (300 - button_width) // 2

    # Action buttons for managing books: Add, Edit, Delete, View, and Rent.
    add_book_button = ctk.CTkButton(
        left_frame,
        text='Add Book',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=200,
        height=30,
        command=lambda: add_book_window(main_root, tabla_information, refresh_treeview)
    )
    add_book_button.place(x=button_x, y=340)

    edit_book_button = ctk.CTkButton(
        left_frame,
        text='Edit Book',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=200,
        height=30,
        command=lambda: messagebox.showinfo(
            'Maintenance',
            "Work is being done on this page",
            parent=main_root
        )
    )
    edit_book_button.place(x=button_x, y=410)

    delete_book_button = ctk.CTkButton(
        left_frame,
        text='Delete Book',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=200,
        height=30,
        command=lambda: delete_item(main_root, tabla_information)
    )
    delete_book_button.place(x=button_x, y=480)

    info_book_button = ctk.CTkButton(
        left_frame,
        text='Book Information',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=200,
        height=30,
        command=lambda: messagebox.showinfo(
            'Maintenance',
            "Work is being done on this page",
            parent=main_root
        )
    )
    info_book_button.place(x=button_x, y=550)

    rent_book_button = ctk.CTkButton(
        left_frame,
        text='Rent Book',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=200,
        height=30,
        command=lambda: messagebox.showinfo(
            'Maintenance',
            "Work is being done on this page",
            parent=main_root
        )
    )
    rent_book_button.place(x=button_x, y=620)

    # Function to fetch and display book records from the database.
    def populate_treeview():
        """
        Connects to the SQLite database, retrieves all book records, and inserts them into the treeview.
        """
        try:
            connection = sqlite3.connect('./db/bookstore_management.db')
            cursor = connection.cursor()
            query = """
            SELECT book_id, book_name, book_publisher, author_name, 
                   book_year, book_genre, book_language, book_ISBN, book_quantity 
            FROM books;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                tabla_information.insert("", "end", values=row)

            cursor.close()
            connection.close()
        except sqlite3.Error as err:
            print(f"Error: {err}")

    # Populate the treeview with existing book records upon initialization.
    populate_treeview()

    # Function to refresh the treeview, clearing existing entries and re-fetching from the database.
    def refresh_treeview(tabla_information):
        """
        Refreshes the treeview by clearing existing entries and fetching updated data from the database.

        Parameters:
        - tabla_information: The treeview widget to be refreshed.
        """
        for item in tabla_information.get_children():
            tabla_information.delete(item)

        try:
            conn = sqlite3.connect('./db/bookstore_management.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT book_id, book_name, book_publisher, author_name, book_year, book_genre, book_language, book_ISBN, book_quantity FROM books')
            rows = cursor.fetchall()

            for row in rows:
                tabla_information.insert("", "end", values=row)

            conn.close()
        except sqlite3.Error as err:
            print(f"Error refreshing treeview: {err}")

    # Start the application's main event loop.
    main_root.mainloop()


# Execute the main_window function to launch the application.
if __name__ == "__main__":
    main_window()
