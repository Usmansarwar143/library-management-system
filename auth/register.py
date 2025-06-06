import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from database.db_config import Database
from utils.security import Security
from utils.validators import Validators

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.security = Security()
        self.validators = Validators()
        # Apply a modern theme
        self.style = Style(theme='flatly')  # Using 'flatly' for a clean, modern look
        self.root.title("Library Management System - Register")
        self.root.geometry("1000x1000")  # Match LoginWindow size for consistency
        self.create_gui()

    def create_gui(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container with card-like styling
        main_frame = ttk.Frame(self.root, padding=20, bootstyle="light")
        main_frame.pack(fill="both", expand=True)

        # Card container for the registration form
        card_frame = ttk.Frame(main_frame, padding=20, bootstyle="light", relief="raised", borderwidth=2)
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        # Title
        ttk.Label(
            card_frame,
            text="Register",
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

        # Role
        ttk.Label(card_frame, text="Role", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        self.role_var = tk.StringVar(value="user")
        ttk.Radiobutton(
            card_frame,
            text="User",
            variable=self.role_var,
            value="user",
            bootstyle="primary"
        ).pack(anchor="w", pady=5)
        ttk.Radiobutton(
            card_frame,
            text="Admin",
            variable=self.role_var,
            value="admin",
            bootstyle="primary"
        ).pack(anchor="w", pady=5)

        # Register Button
        ttk.Button(
            card_frame,
            text="Register",
            command=self.register,
            bootstyle="success",
            width=15
        ).pack(pady=20)

        # Back to Login
        ttk.Button(
            card_frame,
            text="Back to Login",
            command=self.back_to_login,
            bootstyle="primary-link"
        ).pack()

        # Bind Enter key to register
        self.password_entry.bind("<Return>", lambda event: self.register())

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields", parent=self.root)
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=self.root)
            return

        try:
            cursor = self.db.get_connection().cursor()
            hashed_password = self.security.hash_password(password)
            cursor.execute(
                "INSERT INTO USERS (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_password, role)
            )
            self.db.get_connection().commit()
            messagebox.showinfo("Success", "Registration successful", parent=self.root)
            self.back_to_login()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}", parent=self.root)
        finally:
            cursor.close()

    def back_to_login(self):
        from auth.login import LoginWindow
        LoginWindow(self.root)