import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from database.db_config import Database
from modules.books import BookManager
from modules.members import MemberManager
from modules.transactions import TransactionManager
import pandas as pd
from datetime import datetime

class AdminDashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.db = Database()
        self.book_manager = BookManager()
        self.member_manager = MemberManager()
        self.transaction_manager = TransactionManager()
        # Apply a modern theme
        self.style = Style(theme='flatly')  # Using 'flatly' for a clean, modern look
        self.root.title("Library Management System")
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
        books_menu.add_command(label="Add Book", command=self.add_book)
        books_menu.add_command(label="Search Books", command=self.search_books)
        books_menu.add_command(label="View All Books", command=self.view_books)

        # Members Menu
        members_menu = tk.Menu(menubar, tearoff=0, bg="#f8f9fa", font=("Helvetica", 10))
        menubar.add_cascade(label="Members", menu=members_menu)
        members_menu.add_command(label="Add Member", command=self.add_member)
        members_menu.add_command(label="View Members", command=self.view_members)

        # Transactions Menu
        transactions_menu = tk.Menu(menubar, tearoff=0, bg="#f8f9fa", font=("Helvetica", 10))
        menubar.add_cascade(label="Transactions", menu=transactions_menu)
        transactions_menu.add_command(label="Issue Book", command=self.issue_book)
        transactions_menu.add_command(label="Return Book", command=self.return_book)
        transactions_menu.add_command(label="View Issued Books", command=self.view_issued_books)

        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0, bg="#f8f9fa", font=("Helvetica", 10))
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Overdue Books", command=self.view_overdue_books)
        reports_menu.add_command(label="Fine Summary", command=self.fine_summary)
        reports_menu.add_command(label="Export to CSV", command=self.export_to_csv)

        # Logout
        menubar.add_command(label="Logout", command=self.logout)

        # Welcome Label
        ttk.Label(
            main_frame,
            text="Library Management Dashboard",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        ).pack(pady=(20, 40))

        # Quick Action Buttons
        button_frame = ttk.Frame(main_frame, bootstyle="light")
        button_frame.pack(fill="x", pady=20)

        ttk.Button(
            button_frame,
            text="Add Book",
            command=self.add_book,
            bootstyle="primary-outline",
            width=15
        ).pack(side="left", padx=10)
        ttk.Button(
            button_frame,
            text="Add Member",
            command=self.add_member,
            bootstyle="success-outline",
            width=15
        ).pack(side="left", padx=10)
        ttk.Button(
            button_frame,
            text="Issue Book",
            command=self.issue_book,
            bootstyle="info-outline",
            width=15
        ).pack(side="left", padx=10)
        ttk.Button(
            button_frame,
            text="View Books",
            command=self.view_books,
            bootstyle="secondary-outline",
            width=15
        ).pack(side="left", padx=10)

    def add_book(self):
        win = ttk.Toplevel(self.root)
        win.title("Add New Book")
        win.geometry("400x450")
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Form fields
        ttk.Label(frame, text="Title", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        title_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        title_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Author", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        author_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        author_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Category", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        category_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        category_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Quantity", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        quantity_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        quantity_entry.pack(fill="x", pady=5)

        def save_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            category = category_entry.get().strip()
            quantity = quantity_entry.get().strip()

            if not all([title, author, category, quantity]):
                messagebox.showerror("Error", "Please fill all fields", parent=win)
                return

            if not quantity.isdigit() or int(quantity) < 0:
                messagebox.showerror("Error", "Invalid quantity", parent=win)
                return

            try:
                self.book_manager.add_book(title, author, category, int(quantity))
                messagebox.showinfo("Success", "Book added successfully", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {e}", parent=win)

        ttk.Button(
            frame,
            text="Save Book",
            command=save_book,
            bootstyle="success",
            width=15
        ).pack(pady=20)

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

    def add_member(self):
        win = ttk.Toplevel(self.root)
        win.title("Add New Member")
        win.geometry("400x450")
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Name", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        name_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        name_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Email", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        email_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        email_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Phone", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        phone_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        phone_entry.pack(fill="x", pady=5)

        def save_member():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()

            if not all([name, email]):
                messagebox.showerror("Error", "Name and Email are required", parent=win)
                return

            if not Validators.validate_email(email):
                messagebox.showerror("Error", "Invalid email format", parent=win)
                return

            if phone and not Validators.validate_phone(phone):
                messagebox.showerror("Error", "Invalid phone format", parent=win)
                return

            try:
                self.member_manager.add_member(name, email, phone)
                messagebox.showinfo("Success", "Member added successfully", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {e}", parent=win)

        ttk.Button(
            frame,
            text="Save Member",
            command=save_member,
            bootstyle="success",
            width=15
        ).pack(pady=20)

    def view_members(self):
        win = ttk.Toplevel(self.root)
        win.title("All Members")
        win.geometry("700x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Treeview with Scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Email", "Phone"),
            show="headings",
            bootstyle="primary"
        )
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Phone", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Alternating row colors
        tree.tag_configure("oddrow", background="#f8f9fa")
        tree.tag_configure("evenrow", background="#ffffff")

        members = self.member_manager.get_all_members()
        for i, member in enumerate(members):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=member, tags=(tag,))

    def issue_book(self):
        win = ttk.Toplevel(self.root)
        win.title("Issue Book")
        win.geometry("400x350")
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Book ID", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        book_id_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        book_id_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Member ID", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        member_id_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        member_id_entry.pack(fill="x", pady=5)

        def issue():
            book_id = book_id_entry.get().strip()
            member_id = member_id_entry.get().strip()

            if not all([book_id, member_id]):
                messagebox.showerror("Error", "Please fill all fields", parent=win)
                return

            try:
                book_id = int(book_id)
                member_id = int(member_id)
                self.transaction_manager.issue_book(book_id, member_id)
                messagebox.showinfo("Success", "Book issued successfully", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to issue book: {e}", parent=win)

        ttk.Button(
            frame,
            text="Issue Book",
            command=issue,
            bootstyle="success",
            width=15
        ).pack(pady=20)

    def return_book(self):
        win = ttk.Toplevel(self.root)
        win.title("Return Book")
        win.geometry("400x300")
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Transaction ID", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        txn_id_entry = ttk.Entry(frame, width=30, font=("Helvetica", 10))
        txn_id_entry.pack(fill="x", pady=5)

        def return_book():
            txn_id = txn_id_entry.get().strip()

            if not txn_id:
                messagebox.showerror("Error", "Please enter transaction ID", parent=win)
                return

            try:
                txn_id = int(txn_id)
                fine = self.transaction_manager.return_book(txn_id)
                messagebox.showinfo("Success", f"Book returned. Fine: ${fine:.2f}", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book: {e}", parent=win)

        ttk.Button(
            frame,
            text="Return Book",
            command=return_book,
            bootstyle="success",
            width=15
        ).pack(pady=20)

    def view_issued_books(self):
        win = ttk.Toplevel(self.root)
        win.title("Issued Books")
        win.geometry("900x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Treeview with Scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Book", "Member", "Issue Date", "Return Date", "Fine"),
            show="headings",
            bootstyle="primary"
        )
        tree.heading("ID", text="ID")
        tree.heading("Book", text="Book")
        tree.heading("Member", text="Member")
        tree.heading("Issue Date", text="Issue Date")
        tree.heading("Return Date", text="Return Date")
        tree.heading("Fine", text="Fine")
        tree.column("ID", width=50)
        tree.column("Book", width=200)
        tree.column("Member", width=150)
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

        transactions = self.transaction_manager.get_issued_books()
        for i, txn in enumerate(transactions):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=txn, tags=(tag,))

    def view_overdue_books(self):
        win = ttk.Toplevel(self.root)
        win.title("Overdue Books")
        win.geometry("900x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        # Treeview with Scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Book", "Member", "Issue Date", "Return Date", "Fine"),
            show="headings",
            bootstyle="primary"
        )
        tree.heading("ID", text="ID")
        tree.heading("Book", text="Book")
        tree.heading("Member", text="Member")
        tree.heading("Issue Date", text="Issue Date")
        tree.heading("Return Date", text="Return Date")
        tree.heading("Fine", text="Fine")
        tree.column("ID", width=50)
        tree.column("Book", width=200)
        tree.column("Member", width=150)
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

        transactions = self.transaction_manager.get_overdue_books()
        for i, txn in enumerate(transactions):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=txn, tags=(tag,))

    def fine_summary(self):
        win = ttk.Toplevel(self.root)
        win.title("Fine Summary")
        win.geometry("400x300")
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=20, bootstyle="light")
        frame.pack(fill="both", expand=True)

        total_fines = self.transaction_manager.get_total_fines()
        ttk.Label(
            frame,
            text=f"Total Fines Collected: ${total_fines:.2f}",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        ).pack(pady=30)

        ttk.Button(
            frame,
            text="Close",
            command=win.destroy,
            bootstyle="secondary",
            width=15
        ).pack(pady=20)

    def export_to_csv(self):
        try:
            transactions = self.transaction_manager.get_issued_books()
            df = pd.DataFrame(transactions, columns=["ID", "Book", "Member", "Issue Date", "Return Date", "Fine"])
            df.to_csv("library_transactions.csv", index=False)
            messagebox.showinfo("Success", "Data exported to library_transactions.csv", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}", parent=self.root)

    def logout(self):
        from auth.login import LoginWindow
        LoginWindow(self.root)