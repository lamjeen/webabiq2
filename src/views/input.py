"""
Input screen for transactions.
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from src.utils.validation import validate_amount
from src.views.components.background_frame import BackgroundFrame
from src.views.components.header_frame import HeaderFrame
from src.views.components.transaction_type_frame import TransactionTypeFrame
from src.views.components.input_frame import InputFrame

class InputScreen(tk.Frame):
    def __init__(self, parent, account_data, on_complete=None, on_back=None):
        super().__init__(parent)
        self.parent = parent
        self.account_data = account_data
        self.on_complete = on_complete
        self.on_back = on_back
        
        self.setup_ui()
        self.pack(fill="both", expand=True)
    
    def setup_ui(self):
        """Setup the user interface components"""
        # Background image (placed first to be at the bottom)
        bg_path = os.path.join("assets", "bg1.png")
        self.bg_frame = BackgroundFrame(self, bg_path)
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main content container
        self.content_frame = tk.Frame(self)
        self.content_frame.configure(bg='')  # Transparent
        self.content_frame.pack(fill="both", expand=True)
        
        # Header
        self.header = HeaderFrame(
            self.content_frame,
            "Input",
            self.return_to_account
        )
        self.header.pack(fill="x", padx=20, pady=20)
        
        # Transaction type
        self.type_frame = TransactionTypeFrame(self.content_frame)
        self.type_frame.pack(fill="x", padx=20, pady=10)
        
        # Input fields
        self.setup_input_fields()
        
        # Save button
        self.setup_save_button()
    
    def setup_input_fields(self):
        """Setup input fields for date, amount, and description"""
        # Date input
        date_frame = InputFrame(self.content_frame, "DATE")
        date_frame.pack(fill="x", padx=20, pady=10)
        
        self.date_entry = tk.Entry(
            date_frame.content,
            font=("Arial", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0
        )
        self.date_entry.pack(fill="x")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Amount input
        amount_frame = InputFrame(self.content_frame, "AMOUNT")
        amount_frame.pack(fill="x", padx=20, pady=10)
        
        self.amount_entry = tk.Entry(
            amount_frame.content,
            font=("Arial", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0
        )
        self.amount_entry.pack(fill="x")
        
        # Description input
        description_frame = InputFrame(self.content_frame, "DESCRIPTION")
        description_frame.pack(fill="x", padx=20, pady=10)
        
        self.description_text = tk.Text(
            description_frame.content,
            font=("Arial", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0,
            height=8
        )
        self.description_text.pack(fill="both")
    
    def setup_save_button(self):
        """Setup save button"""
        tk.Button(
            self.content_frame,
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
            category=self.type_frame.get_type(),
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