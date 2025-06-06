import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from database.db_config import Database
from modules.books import BookManager
from modules.transactions import TransactionManager

class UserDashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.db = Database()
        self.book_manager = BookManager()
        self.transaction_manager = TransactionManager()
        # Apply a modern theme
        self.style = Style(theme='flatly')  # Using 'flatly' for a clean, modern look
        self.root.title("Library Management System - User Dashboard")
        self.root.geometry("800x600")  # Set a default window size
        self.create_gui()

    def create_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        main_frame = ttk.Frame(self.root, padding=20, bootstyle="light")
        main_frame.pack(fill="both", expand=True)

        # Menu Bar
        menubar = tk.Menu(self.root, bg="#f8f9fa", font=("Helvetica", 10))
        self.root.config(menu=menubar)

        # Books Menu
        books_menu = tk.Menu(menubar, tearoff=0, bg="#f8f9fa", font=("Helvetica", 10))
        menubar.add_cascade(label="Books", menu=books_menu)
        books_menu.add_command(label="Search Books", command=self.search_books)
        books_menu.add_command(label="View All Books", command=self.view_books)

        # Transactions Menu
        transactions_menu = tk.Menu(menubar, tearoff=0, bg="#f8f9fa", font=("Helvetica", 10))
        menubar.add_cascade(label="Transactions", menu=transactions_menu)
        transactions_menu.add_command(label="My Books", command=self.view_my_books)

        # Logout
        menubar.add_command(label="Logout", command=self.logout)

        # Welcome Label
        ttk.Label(
            main_frame,
            text="User Dashboard",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        ).pack(pady=(20, 40))

        # Quick Action Buttons
        button_frame = ttk.Frame(main_frame, bootstyle="light")
        button_frame.pack(fill="x", pady=20)

        ttk.Button(
            button_frame,
            text="Search Books",
            command=self.search_books,
            bootstyle="primary-outline",
            width=15
        ).pack(side="left", padx=10)
        ttk.Button(
            button_frame,
            text="View All Books",
            command=self.view_books,
            bootstyle="info-outline",
            width=15
        ).pack(side="left", padx=10)
        ttk.Button(
            button_frame,
            text="My Books",
            command=self.view_my_books,
            bootstyle="success-outline",
            width=15
        ).pack(side="left", padx=10)

    def search_books(self):
        win = ttk.Toplevel(self.root)
        win.title("Search Books")
        win.geometry("700x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Search bar
        search_frame = ttk.Frame(frame, bootstyle="light")
        search_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(search_frame, text="Search by Title", font=("Helvetica", 12)).pack(side="left")
        search_entry = ttk.Entry(search_frame, width=30, font=("Helvetica", 10))
        search_entry.pack(side="left", padx=10)
        ttk.Button(
            search_frame,
            text="Search",
            command=lambda: perform_search(),
            bootstyle="primary"
        ).pack(side="left")

        # Treeview with Scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Title", "Author", "Category", "Quantity"),
            show="headings",
            bootstyle="primary"
        )
        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Category", text="Category")
        tree.heading("Quantity", text="Quantity")
        tree.column("ID", width=50)
        tree.column("Title", width=200)
        tree.column("Author", width=150)
        tree.column("Category", width=150)
        tree.column("Quantity", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Alternating row colors
        tree.tag_configure("oddrow", background="#f8f9fa")
        tree.tag_configure("evenrow", background="#ffffff")

        def perform_search():
            query = search_entry.get().strip()
            books = self.book_manager.search_books(query)
            for item in tree.get_children():
                tree.delete(item)
            for i, book in enumerate(books):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                tree.insert("", "end", values=book, tags=(tag,))

        search_entry.bind("<Return>", lambda event: perform_search())

    def view_books(self):
        win = ttk.Toplevel(self.root)
        win.title("All Books")
        win.geometry("700x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Treeview with Scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Title", "Author", "Category", "Quantity"),
            show="headings",
            bootstyle="primary"
        )
        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Category", text="Category")
        tree.heading("Quantity", text="Quantity")
        tree.column("ID", width=50)
        tree.column("Title", width=200)
        tree.column("Author", width=150)
        tree.column("Category", width=150)
        tree.column("Quantity", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Alternating row colors
        tree.tag_configure("oddrow", background="#f8f9fa")
        tree.tag_configure("evenrow", background="#ffffff")

        books = self.book_manager.get_all_books()
        for i, book in enumerate(books):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=book, tags=(tag,))

    def view_my_books(self):
        win = ttk.Toplevel(self.root)
        win.title("My Books")
        win.geometry("900x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Treeview with Scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Book", "Issue Date", "Return Date", "Fine"),
            show="headings",
            bootstyle="primary"
        )
        tree.heading("ID", text="ID")
        tree.heading("Book", text="Book")
        tree.heading("Issue Date", text="Issue Date")
        tree.heading("Return Date", text="Return Date")
        tree.heading("Fine", text="Fine")
        tree.column("ID", width=50)
        tree.column("Book", width=200)
        tree.column("Issue Date", width=100)
        tree.column("Return Date", width=100)
        tree.column("Fine", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Alternating row colors
        tree.tag_configure("oddrow", background="#f8f9fa")
        tree.tag_configure("evenrow", background="#ffffff")

        cursor = self.db.get_connection().cursor()
        cursor.execute("""
            SELECT t.txn_id, b.title, t.issue_date, t.return_date, t.fine
            FROM TRANSACTIONS t
            JOIN BOOKS b ON t.book_id = b.book_id
            WHERE t.member_id = %s AND t.actual_return_date IS NULL
        """, (self.user_id,))
        transactions = cursor.fetchall()
        cursor.close()

        for i, txn in enumerate(transactions):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=txn, tags=(tag,))

    def logout(self):
        from auth.login import LoginWindow
        LoginWindow(self.root)