"""
Header frame component with back button and title.
"""
import tkinter as tk

class HeaderFrame(tk.Frame):
    def __init__(self, parent, title, on_back):
        super().__init__(parent)
        self.configure(bg='')  # Transparent
        
        # Back button
        tk.Button(
            self,
            text="←",
            font=("Arial", 24),
            bg="#FFE5E5",
            fg="#E75480",
            bd=0,
            command=on_back,
            cursor="hand2"
        ).pack(side="left")
        
        # Title
        tk.Label(
            self,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#FFE5E5",
            fg="#E75480"
        ).pack(side="left", padx=20)