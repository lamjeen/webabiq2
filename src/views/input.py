"""
Input screen for transactions.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.constants import (
    PINK_GRADIENT_START,
    PINK_GRADIENT_END,
    PINK_BUTTON,
    LIGHT_CREAM,
    DARK_TEXT
)
from src.utils.validation import validate_amount

class InputScreen(tk.Frame):
    def __init__(self, parent, account_data, on_complete=None, on_back=None):
        super().__init__(parent)
        self.parent = parent
        self.account_data = account_data
        self.on_complete = on_complete
        self.on_back = on_back
        
        # Initialize UI
        self.setup_ui()
        self.pack(fill="both", expand=True)
    
    def setup_ui(self):
        """Setup the user interface components"""
        # Create gradient background (yellow to pink)
        self.configure(bg="#FFE5E5")
        
        # Header with back button and title
        header_frame = tk.Frame(self, bg="#FFE5E5")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=("Arial", 24),
            bg="#FFE5E5",
            fg="#E75480",
            bd=0,
            command=self.return_to_account,
            cursor="hand2"
        )
        back_button.pack(side="left")
        
        tk.Label(
            header_frame,
            text="input",
            font=("Arial", 24, "bold"),
            bg="#FFE5E5",
            fg="#E75480"
        ).pack(side="left", padx=20)
        
        # Transaction type toggle
        type_frame = tk.Frame(self, bg="white", bd=0)
        type_frame.pack(fill="x", padx=20, pady=10)
        
        self.transaction_type = tk.StringVar(value="Income")
        
        paid_button = tk.Radiobutton(
            type_frame,
            text="PAID",
            variable=self.transaction_type,
            value="Paid",
            bg="white",
            fg="#666666",
            font=("Arial", 12, "bold"),
            selectcolor="white",
            indicatoron=False,
            width=15,
            pady=10
        )
        paid_button.pack(side="left", expand=True)
        
        income_button = tk.Radiobutton(
            type_frame,
            text="INCOME",
            variable=self.transaction_type,
            value="Income",
            bg="#E75480",
            fg="white",
            font=("Arial", 12, "bold"),
            selectcolor="#E75480",
            indicatoron=False,
            width=15,
            pady=10
        )
        income_button.pack(side="right", expand=True)
        
        # Date input
        date_frame = tk.Frame(self, bg="#E75480", bd=0)
        date_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            date_frame,
            text="DATE",
            font=("Arial", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=20, pady=15)
        
        self.date_entry = tk.Entry(
            date_frame,
            font=("Arial", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0
        )
        self.date_entry.pack(side="right", padx=20, pady=15, fill="x", expand=True)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Amount input
        amount_frame = tk.Frame(self, bg="#E75480", bd=0)
        amount_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            amount_frame,
            text="AMOUNT",
            font=("Arial", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=20, pady=15)
        
        self.amount_entry = tk.Entry(
            amount_frame,
            font=("Arial", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0
        )
        self.amount_entry.pack(side="right", padx=20, pady=15, fill="x", expand=True)
        
        # Description input
        description_frame = tk.Frame(self, bg="#E75480", bd=0)
        description_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            description_frame,
            text="DESCRIPTION",
            font=("Arial", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.description_text = tk.Text(
            description_frame,
            font=("Arial", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0,
            height=8
        )
        self.description_text.pack(padx=20, pady=(5, 15), fill="both")
        
        # Save button at the bottom
        tk.Button(
            self,
            text="SAVE",
            command=self.save_transaction,
            bg="#E75480",
            fg="white",
            font=("Arial", 14, "bold"),
            bd=0,
            pady=10,
            cursor="hand2"
        ).pack(side="bottom", fill="x", padx=20, pady=20)
    
    def save_transaction(self):
        """Save the transaction and close the window"""
        # Validate amount
        amount_str = self.amount_entry.get().strip()
        is_valid, amount = validate_amount(amount_str)
        
        if not is_valid:
            messagebox.showerror("Error", amount)
            return
        
        # Get description
        description = self.description_text.get("1.0", "end-1c").strip()
        if not description:
            messagebox.showerror("Error", "Description is required")
            return
        
        # Get date
        try:
            date_str = self.date_entry.get()
            transaction_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        
        # Add transaction
        self.account_data.add_transaction(
            amount=amount,
            category=self.transaction_type.get(),
            description=description,
            date=transaction_date
        )
        
        # Destroy this screen and trigger callback
        self.pack_forget()
        if self.on_complete:
            self.on_complete()
    
    def return_to_account(self):
        """Return to account book page"""
        self.pack_forget()
        if self.on_back:
            self.on_back()