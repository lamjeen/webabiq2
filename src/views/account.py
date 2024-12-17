"""
Main account screen view.
"""
import tkinter as tk
from datetime import datetime
from src.constants import PINK_BUTTON
from src.views.input import InputScreen

class AccountScreen(tk.Frame):
    def __init__(self, parent, account_data):
        super().__init__(parent)
        self.parent = parent
        self.account_data = account_data
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.create_widgets()
        self.update_displays()
    
    # Rest of the implementation remains the same as in run2.py
    # Just update imports to use the new modular structure