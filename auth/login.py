import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from database.db_config import Database
from utils.security import Security
from dashboard.admin_dashboard import AdminDashboard
from dashboard.user_dashboard import UserDashboard

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.security = Security()
        # Apply a modern theme
        self.style = Style(theme='flatly')  # Using 'flatly' for a clean, modern look
        self.root.title("Library Management System - Login")
        self.root.geometry("1000x1000")  # Increased window size for a more spacious interface
        self.create_gui()

    def create_gui(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container with card-like styling
        main_frame = ttk.Frame(self.root, padding=20, bootstyle="light")
        main_frame.pack(fill="both", expand=True)

        # Card container for the login form
        card_frame = ttk.Frame(main_frame, padding=20, bootstyle="light", relief="raised", borderwidth=2)
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Title
        ttk.Label(
            card_frame,
            text="Library Management System",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        ).pack(pady=(20, 30))

        # Username
        ttk.Label(card_frame, text="Username", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        self.username_entry = ttk.Entry(card_frame, width=30, font=("Helvetica", 10))
        self.username_entry.pack(fill="x", pady=5)

        # Password
        ttk.Label(card_frame, text="Password", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(card_frame, show="*", width=30, font=("Helvetica", 10))
        self.password_entry.pack(fill="x", pady=5)

        # Login Button
        ttk.Button(
            card_frame,
            text="Login",
            command=self.login,
            bootstyle="success",
            width=15
        ).pack(pady=20)

        # Register Link
        ttk.Button(
            card_frame,
            text="Register",
            command=self.open_register,
            bootstyle="primary-link"
        ).pack()

        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields", parent=self.root)
            return

        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT user_id, password, role FROM USERS WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and self.security.verify_password(password, user[1]):
                if user[2] == 'admin':
                    AdminDashboard(self.root, user[0])
                else:
                    UserDashboard(self.root, user[0])
            else:
                messagebox.showerror("Error", "Invalid credentials", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {e}", parent=self.root)
        finally:
            cursor.close()

    def open_register(self):
        from auth.register import RegisterWindow
        RegisterWindow(self.root)