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
    
    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text="account book",
            font=("Arial", 32, "bold"),
            bg="#FFB6C1",
            fg="#E75480"
        ).pack(pady=(20, 10))
        
        tk.Label(
            self,
            text=self.account_data.today_date,
            font=("Arial", 14),
            bg="#FFB6C1",
            fg="#666666"
        ).pack(pady=(0, 20))
        
        # Monthly overview
        month_frame = tk.Frame(self, bg="white", padx=30, pady=15)
        month_frame.pack(fill="x", padx=20)
        
        tk.Label(
            month_frame,
            text="THIS MONTH",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(side="left")
        
        self.saving_label = tk.Label(
            month_frame,
            text=f"${self.account_data.total_saving:.2f}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#E75480"
        )
        self.saving_label.pack(side="right")
        
        # Transaction buttons
        buttons_frame = tk.Frame(self, bg="#FFB6C1")
        buttons_frame.pack(pady=20)
        
        # Income button
        income_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
        income_frame.pack(side="left", padx=10)
        
        tk.Label(
            income_frame,
            text="INCOME",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=5)
        
        self.income_label = tk.Label(
            income_frame,
            text=f"${self.account_data.income:.2f}",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        )
        self.income_label.pack(side="right", padx=5)
        
        # Paid button
        paid_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
        paid_frame.pack(side="left", padx=10)
        
        tk.Label(
            paid_frame,
            text="PAID",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=5)
        
        self.paid_label = tk.Label(
            paid_frame,
            text=f"${self.account_data.paid:.2f}",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        )
        self.paid_label.pack(side="right", padx=5)
        
        # Enter button
        tk.Button(
            self,
            text="Enter!",
            font=("Arial", 16, "bold"),
            bg="#FFE4E1",
            fg="#E75480",
            relief="flat",
            padx=40,
            pady=10,
            command=self.show_entry_dialog
        ).pack(pady=20)
        
        # Monthly stats
        monthly_frame = tk.Frame(self, bg="#E75480")
        monthly_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            monthly_frame,
            text=str(datetime.now().year),
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(fill="x", pady=5)
        
        month_info_frame = tk.Frame(monthly_frame, bg="#E75480")
        month_info_frame.pack(fill="x", pady=5)
        
        self.monthly_range_label = tk.Label(
            month_info_frame,
            text=self.account_data.monthly_range,
            font=("Arial", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_range_label.pack(side="left", padx=20)
        
        self.monthly_amount_label = tk.Label(
            month_info_frame,
            text=f"${self.account_data.monthly_total:.2f}",
            font=("Arial", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_amount_label.pack(side="right", padx=20)
        
        # Transaction history
        headers_frame = tk.Frame(self, bg="#E75480")
        headers_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        headers = ["DATE", "INCOME/PAID", "DESCRIPTION"]
        for header in headers:
            tk.Label(
                headers_frame,
                text=header,
                font=("Arial", 10, "bold"),
                bg="#E75480",
                fg="white",
                width=15
            ).pack(side="left", padx=5, pady=5)
        
        self.transactions_frame = tk.Frame(self, bg="white")
        self.transactions_frame.pack(fill="both", expand=True, padx=20)
    
    def show_entry_dialog(self):
        # Hide the main window
        self.parent.withdraw()
        
        # Create and show the input screen
        input_screen = InputScreen(
            tk.Toplevel(self.parent),
            self.account_data,
            on_complete=self.handle_transaction_complete
        )
        input_screen.pack(fill="both", expand=True)
    
    def handle_transaction_complete(self):
        self.update_displays()
        self.parent.deiconify()
    
    def update_displays(self):
        self.saving_label.config(text=f"${self.account_data.total_saving:.2f}")
        self.income_label.config(text=f"${self.account_data.income:.2f}")
        self.paid_label.config(text=f"${self.account_data.paid:.2f}")
        self.monthly_amount_label.config(text=f"${self.account_data.monthly_total:.2f}")
        
        # Update history
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
            
        for transaction in reversed(self.account_data.monthly_transactions):
            row = tk.Frame(self.transactions_frame, bg="white")
            row.pack(fill="x", pady=1)
            
            sign = "+" if transaction['category'] == "Income" else "-"
            
            tk.Label(
                row,
                text=transaction['date'].strftime("%Y-%m-%d"),
                bg="white",
                width=15
            ).pack(side="left", padx=5)
            
            tk.Label(
                row,
                text=f"{sign}${transaction['amount']:.2f}",
                bg="white",
                width=15,
                fg="#E75480" if sign == "+" else "#666666"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row,
                text=transaction['description'],
                bg="white",
                width=15
            ).pack(side="left", padx=5)