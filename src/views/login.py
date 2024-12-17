"""
Login screen view.
"""
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from src.constants import PINK_BUTTON, LIGHT_CREAM
from src.utils.auth import validate_credentials

class LoginScreen(tk.Frame):
    def __init__(self, parent, credentials):
        super().__init__(parent)
        self.parent = parent
        self.credentials = credentials
        self.login_success_callback = None
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.login_container = tk.Frame(
            self,
            bg="white",
            highlightthickness=0
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Implementation remains the same as in run2.py
        # Just update imports to use constants from src.constants
        pass