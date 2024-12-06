import customtkinter as ctk
import tkinter.messagebox as messagebox


# Function to create a new window for adding books
def add_book_window(main_root):
    # Create the "Add Book" window as a Toplevel window
    add_book_root = ctk.CTkToplevel(main_root)
    add_book_root.geometry('400x600')
    ctk.set_default_color_theme('dark-blue')  # Set default theme
    add_book_root.resizable(False, False)
    add_book_root.after(200, lambda: add_book_root.iconbitmap('./images/icobookstore.ico'))
    add_book_root.title('BooksTore')

    # Center the "Add Book" window on the screen
    screen_width = add_book_root.winfo_screenwidth()
    screen_height = add_book_root.winfo_screenheight()
    window_width = 400
    window_height = 600
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    add_book_root.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    # Make the "Add Book" window modal
    add_book_root.transient(main_root)
    add_book_root.grab_set()
    add_book_root.lift()
    add_book_root.attributes('-topmost', True)

    # Labels and entry fields for book information
    bookname_label = ctk.CTkLabel(add_book_root, text='Book Name:', font=('Cascadia Code', 14))
    bookname_label.place(x=30, y=50)
    bookname_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    bookname_entry.place(x=185, y=50)

    publisher_label = ctk.CTkLabel(add_book_root, text='Publisher Name:', font=('Cascadia Code', 14))
    publisher_label.place(x=30, y=100)
    publisher_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    publisher_entry.place(x=185, y=100)

    author_label = ctk.CTkLabel(add_book_root, text='Author Name:', font=('Cascadia Code', 14))
    author_label.place(x=30, y=145)
    author_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    author_entry.place(x=185, y=145)

    book_year_label = ctk.CTkLabel(add_book_root, text='Book Year:', font=('Cascadia Code', 14))
    book_year_label.place(x=30, y=190)
    book_year_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    book_year_entry.place(x=185, y=190)

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

    category_label = ctk.CTkLabel(add_book_root, text='Category:', font=('Cascadia Code', 14))
    category_label.place(x=30, y=280)
    category_cbx = ctk.CTkComboBox(
        add_book_root,
        values=['Fiction', 'Non-Fiction', 'Reference Books', 'Textbooks or Educational Books', 'Technical or Specialized Books', 'Magazines and Periodicals', 'Other'],
        dropdown_hover_color='#4c2c18',
        dropdown_font=('Cascadia Code', 12),
        font=('Cascadia Code', 12),
        width=190
    )
    category_cbx.set('')
    category_cbx.place(x=185, y=280)

    isbn_label = ctk.CTkLabel(add_book_root, text='Book ISBN:', font=('Cascadia Code', 14))
    isbn_label.place(x=30, y=325)
    isbn_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    isbn_entry.place(x=185, y=325)

    quantity_label = ctk.CTkLabel(add_book_root, text='Book Quantity:', font=('Cascadia Code', 14))
    quantity_label.place(x=30, y=370)
    quantity_entry = ctk.CTkEntry(add_book_root, font=('Cascadia Code', 14), width=190)
    quantity_entry.place(x=185, y=370)

    # Submit button (currently under maintenance)
    submit_button = ctk.CTkButton(
        add_book_root,
        text='Submit',
        fg_color='#605b3e',
        hover_color='#4c2c18',
        font=('Cascadia Code', 14),
        width=150,
        height=30,
        command=lambda: messagebox.showinfo('Maintenance', "Work is being done on this page", parent=add_book_root)
    )
    submit_button.place(x=30, y=500)

    # Clear button to reset all fields
    def clear_info():
        bookname_entry.delete(0, 'end')
        publisher_entry.delete(0, 'end')
        author_entry.delete(0, 'end')
        book_year_entry.delete(0, 'end')
        genre_cbx.set('')
        category_cbx.set('')
        isbn_entry.delete(0, 'end')
        quantity_entry.delete(0, 'end')

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

