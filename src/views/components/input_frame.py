"""
Styled input frame component.
"""
import tkinter as tk

class InputFrame(tk.Frame):
    def __init__(self, parent, label_text, **kwargs):
        super().__init__(parent, bg="#E75480", bd=0)
        
        # Label
        tk.Label(
            self,
            text=label_text,
            font=("Arial", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=20, pady=15)
        
        # Content frame for additional widgets
        self.content = tk.Frame(self, bg="#E75480")
        self.content.pack(side="right", padx=20, pady=15, fill="x", expand=True)