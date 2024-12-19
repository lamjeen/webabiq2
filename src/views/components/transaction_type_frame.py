"""
Transaction type toggle frame component.
"""
import tkinter as tk
from src.components.toggle_button import ToggleButton

class TransactionTypeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", bd=0)
        
        self.transaction_type = tk.StringVar(value="Income")
        
        # Toggle buttons
        self.paid_button = ToggleButton(
            self,
            text="PAID",
            value="Paid",
            variable=self.transaction_type
        )
        self.paid_button.pack(side="left", expand=True)
        
        self.income_button = ToggleButton(
            self,
            text="INCOME",
            value="Income",
            variable=self.transaction_type
        )
        self.income_button.pack(side="right", expand=True)
    
    def get_type(self):
        return self.transaction_type.get()