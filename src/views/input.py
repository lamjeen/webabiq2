"""
Input screen for transactions.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from src.constants import (
    PINK_GRADIENT_START,
    PINK_GRADIENT_END,
    PINK_BUTTON,
    LIGHT_CREAM,
    DARK_TEXT
)
from src.utils.ui import create_gradient_background
from src.utils.validation import validate_amount

class InputScreen(tk.Frame):
    def __init__(self, parent, account_data, on_complete=None):
        super().__init__(parent)
        self.parent = parent
        self.account_data = account_data
        self.on_complete = on_complete
        self.setup_ui()
        
    # Rest of the implementation remains the same as in run2.py
    # Just update imports to use the new modular structure