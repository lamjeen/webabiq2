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
            text="Account Book",
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
            command=self.show_entry_dialog,
            cursor="hand2"
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
        
        # Create a container for the transaction list
        self.list_container = tk.Frame(self, bg="white")
        self.list_container.pack(fill="both", expand=True, padx=20)
        
        # Transaction history headers
        headers_frame = tk.Frame(self.list_container, bg="#E75480")
        headers_frame.pack(fill="x", pady=(0, 1))
        
        # Column configurations
        self.columns = {
            "DATE": {"width": 12, "anchor": "center"},
            "AMOUNT": {"width": 12, "anchor": "center"},
            "DESCRIPTION": {"width": 40, "anchor": "w"}  # Increased width for description
        }
        
        # Create headers
        for header, config in self.columns.items():
            tk.Label(
                headers_frame,
                text=header,
                font=("Arial", 10, "bold"),
                bg="#E75480",
                fg="white",
                width=config["width"],
                anchor=config["anchor"]
            ).pack(side="left", padx=5, pady=5)
        
        # Create scrollable frame for transactions
        self.transactions_canvas = tk.Canvas(
            self.list_container,
            bg="white",
            highlightthickness=0
        )
        self.transactions_canvas.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.transactions_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        
        # Configure canvas
        self.transactions_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame for transaction rows
        self.transactions_frame = tk.Frame(self.transactions_canvas, bg="white")
        self.transactions_canvas.create_window(
            (0, 0),
            window=self.transactions_frame,
            anchor="nw",
            width=self.transactions_canvas.winfo_reqwidth()
        )
        
        # Bind resize event
        self.transactions_frame.bind("<Configure>", self.on_frame_configure)
        self.transactions_canvas.bind("<Configure>", self.on_canvas_configure)
    
    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.transactions_canvas.configure(scrollregion=self.transactions_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        self.transactions_canvas.itemconfig(
            self.transactions_canvas.find_withtag("all")[0],
            width=event.width
        )
    
    def show_entry_dialog(self):
        # Hide the current account screen
        self.pack_forget()
        
        # Create and show the input screen
        input_screen = InputScreen(
            self.parent,
            self.account_data,
            on_complete=self.on_input_complete,
            on_back=self.on_input_back
        )
    
    def on_input_complete(self):
        """Called when input is saved"""
        self.update_displays()
        self.pack(fill="both", expand=True)
    
    def on_input_back(self):
        """Called when back button is pressed"""
        self.pack(fill="both", expand=True)
    
    def update_displays(self):
        self.saving_label.config(text=f"${self.account_data.total_saving:.2f}")
        self.income_label.config(text=f"${self.account_data.income:.2f}")
        self.paid_label.config(text=f"${self.account_data.paid:.2f}")
        self.monthly_amount_label.config(text=f"${self.account_data.monthly_total:.2f}")
        
        # Clear existing transactions
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        
        # Add transactions
        for transaction in reversed(self.account_data.monthly_transactions):
            row = tk.Frame(self.transactions_frame, bg="white")
            row.pack(fill="x", pady=1)
            
            # Date
            tk.Label(
                row,
                text=transaction['date'].strftime("%Y-%m-%d"),
                bg="white",
                width=self.columns["DATE"]["width"],
                anchor=self.columns["DATE"]["anchor"]
            ).pack(side="left", padx=5)
            
            # Amount
            sign = "+" if transaction['category'] == "Income" else "-"
            amount_text = f"{sign}${transaction['amount']:.2f}"
            tk.Label(
                row,
                text=amount_text,
                bg="white",
                width=self.columns["AMOUNT"]["width"],
                anchor=self.columns["AMOUNT"]["anchor"],
                fg="#E75480" if sign == "+" else "#666666"
            ).pack(side="left", padx=5)
            
            # Description (with word wrap)
            description_label = tk.Label(
                row,
                text=transaction['description'],
                bg="white",
                anchor=self.columns["DESCRIPTION"]["anchor"],
                justify="left",
                wraplength=150  # Adjust this value based on your needs
            )
            description_label.pack(side="left", padx=5, fill="x", expand=True)
        
        # Update scroll region
        self.on_frame_configure()