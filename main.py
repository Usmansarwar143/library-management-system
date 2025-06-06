import tkinter as tk
from auth.login import LoginWindow
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def main():
    root = ttk.Window(themename="flatly")
    root.title("Library Management System")
    root.geometry("800x600")
    root.resizable(False, False)
    
    # Center the window
    root.eval('tk::PlaceWindow . center')

    # Start with login window
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()