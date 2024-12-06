import customtkinter as ctk
from PIL import Image
import sys
from tkinter import ttk
from addBookWindow import add_book_window
import tkinter.messagebox as messagebox


# Function to update the user's name label
def update_user_name_label(name_label, username):
    if username:
        name_label.configure(text=f"Welcome, {username.upper()}")
    else:
        name_label.configure(text="Welcome, Guest")


# Main function to display the main application window
def main_window():
    # Create the main window
    main_root = ctk.CTk()
    main_root.geometry('1400x800')
    main_root.resizable(False, False)
    main_root.title('BooksTore')
    ctk.set_default_color_theme('dark-blue')  # Set default theme
    main_root.iconbitmap('./images/icobookstore.ico')

    # Center the window on the screen
    screen_width = main_root.winfo_screenwidth()
    screen_height = main_root.winfo_screenheight()
    window_width = 1400
    window_height = 800
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    main_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')



    # Frame for displaying the table with book information
    treeview_frame = ctk.CTkFrame(main_root, width=1099, height=800)
    treeview_frame.place(x=301, y=0)
    treeview_frame.pack_propagate(False)

    # Scrollbars for the table
    scrollbar_vertical = ctk.CTkScrollbar(treeview_frame, orientation="vertical")
    scrollbar_horizontal = ctk.CTkScrollbar(treeview_frame, orientation="horizontal")

    # Table to display book data
    tabla_information = ttk.Treeview(
        treeview_frame,
        columns=("book_id", "book_name", "book_publisher", "author_name", "book_year", "book_genre", "book_category", "book_language", "book_isbn", "book_quantity"),
        show='headings',
        yscrollcommand=scrollbar_vertical.set,
        xscrollcommand=scrollbar_horizontal.set
    )

    # Setting column headers
    tabla_information.heading('book_id', text='Book ID')
    tabla_information.heading('book_name', text='Book Name')
    tabla_information.heading('book_publisher', text='Publisher')
    tabla_information.heading('author_name', text='Author Name')
    tabla_information.heading('book_year', text='Year')
    tabla_information.heading('book_genre', text='Genre')
    tabla_information.heading('book_category', text='Category')
    tabla_information.heading('book_language', text='Language')
    tabla_information.heading('book_isbn', text='ISBN')
    tabla_information.heading('book_quantity', text='Quantity')

    # Setting column properties
    for column in ("book_id", "book_name", "book_publisher", "author_name", "book_year", "book_genre", "book_category", "book_language", "book_isbn", "book_quantity"):
        tabla_information.column(column, width=200, anchor='center', stretch=False)

    # Configuring and packing scrollbars
    scrollbar_vertical.configure(command=tabla_information.yview)
    scrollbar_horizontal.configure(command=tabla_information.xview)
    scrollbar_vertical.pack(side='left', fill='y')
    scrollbar_horizontal.pack(side='bottom', fill='x')
    tabla_information.pack(side='left', fill='both', expand=True)

    # Adding sample data to the table
    for i in range(100):
        tabla_information.insert('', 'end', values=(f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}", f"Item{i}"))

    # Left panel frame for user actions and info
    left_frame = ctk.CTkFrame(main_root, width=300, height=800, corner_radius=10)
    left_frame.place(x=0, y=0)

    # Footer frame with college information
    foot_frame = ctk.CTkFrame(left_frame, width=300, height=30, fg_color="#4c2c18")
    foot_frame.place(x=0, y=770)
    foot_frame_label = ctk.CTkLabel(
        foot_frame,
        text=' Ivy Tech Community College 2024',
        font=("Cascadia Code", 14),
        text_color='White'
    )
    foot_frame_label.place(x=10, y=0)

    # User avatar or placeholder
    try:
        p_imagen = Image.open('./images/userbook.png')
        r_imagen = ctk.CTkImage(p_imagen, size=(70, 70))
        user_label_imagen = ctk.CTkLabel(left_frame, image=r_imagen, text="")
    except Exception:
        user_label_imagen = ctk.CTkLabel(left_frame, text="Not Found", font=("Cascadia Code", 14, "bold"))
    user_label_imagen.place(x=120, y=50)

    # Display user name
    name_label = ctk.CTkLabel(left_frame, text="User Name", font=('Cascadia Code', 12))
    name_label.place(x=105, y=130)
    username = sys.argv[1] if len(sys.argv) > 1 else None
    update_user_name_label(name_label, username)

    # Search filter dropdown and entry field
    search_filter = ctk.CTkComboBox(
        left_frame,
        values=['Book Name', 'Language', 'ISBN', 'Author Name', 'Publisher', 'Year'],
        width=190,
        height=30,
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12)
    )
    search_filter.set('')
    search_filter.place(x=60, y=200)
    search_entry = ctk.CTkEntry(left_frame, placeholder_text=' Type information')
    search_entry.place(x=60, y=270)

    # Clear search filters
    def clear_command():
        search_filter.set('')
        search_entry.delete(0, 'end')

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

    # Action buttons
    add_book_button = ctk.CTkButton(left_frame, text='Add Book', fg_color='#605b3e', hover_color='#4c2c18', font=('Cascadia Code', 14), width=190, height=30, command=lambda: add_book_window(main_root))
    add_book_button.place(x=60, y=340)

    edit_book_button = ctk.CTkButton(left_frame, text='Edit Book', fg_color='#605b3e', hover_color='#4c2c18', font=('Cascadia Code', 14), width=190, height=30, command=lambda: messagebox.showinfo('Maintenance', "Work is being done on this page", parent=main_root))
    edit_book_button.place(x=60, y=410)

    delete_book_button = ctk.CTkButton(left_frame, text='Delete Book', fg_color='#605b3e', hover_color='#4c2c18', font=('Cascadia Code', 14), width=190, height=30, command=lambda: messagebox.showinfo('Maintenance', "Work is being done on this page", parent=main_root))
    delete_book_button.place(x=60, y=480)

    info_book_button = ctk.CTkButton(left_frame, text='Book Information', fg_color='#605b3e', hover_color='#4c2c18', font=('Cascadia Code', 14), width=190, height=30, command=lambda: messagebox.showinfo('Maintenance', "Work is being done on this page", parent=main_root))
    info_book_button.place(x=60, y=550)

    rent_book_button = ctk.CTkButton(left_frame, text='Rent Book', fg_color='#605b3e', hover_color='#4c2c18', font=('Cascadia Code', 14), width=190, height=30, command=lambda: messagebox.showinfo('Maintenance', "Work is being done on this page", parent=main_root))
    rent_book_button.place(x=60, y=620)

    # Start the main event loop
    main_root.mainloop()


main_window()



