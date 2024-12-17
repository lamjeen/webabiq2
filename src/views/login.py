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
        # Title
        title = tk.Label(
            self.login_container,
            text="webabiq",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#E75480"
        )
        title.pack(pady=(20, 30))
        
        # Username
        tk.Label(
            self.login_container,
            text="USERNAME",
            font=("Arial", 12),
            bg="white",
            fg="#E75480"
        ).pack(anchor="w", padx=20)
        
        self.username_entry = tk.Entry(
            self.login_container,
            font=("Arial", 12),
            bg="#FFE4E1",
            relief="flat",
            width=30
        )
        self.username_entry.pack(padx=20, pady=(0, 20), ipady=8)
        
        # Password
        tk.Label(
            self.login_container,
            text="PASSWORD",
            font=("Arial", 12),
            bg="white",
            fg="#E75480"
        ).pack(anchor="w", padx=20)
        
        self.password_entry = tk.Entry(
            self.login_container,
            font=("Arial", 12),
            bg="#FFE4E1",
            relief="flat",
            width=30,
            show="•"
        )
        self.password_entry.pack(padx=20, pady=(0, 20), ipady=8)
        
        # Bindings
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Remember me
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            self.login_container,
            text="REMEMBER ME",
            variable=self.remember_var,
            bg="white",
            font=("Arial", 10)
        )
        remember_check.pack(pady=(0, 20))
        
        # Login button
        tk.Button(
            self.login_container,
            text="LOG IN",
            command=self.login,
            bg="#E75480",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            width=25,
            cursor="hand2"
        ).pack(pady=(0, 20), ipady=8)
        
        # Forgot password
        forgot_link = tk.Label(
            self.login_container,
            text="FORGOT MY PASSWORD?",
            font=("Arial", 10, "underline"),
            fg="#666666",
            cursor="hand2",
            bg="white"
        )
        forgot_link.pack(pady=(0, 20))
        forgot_link.bind("<Button-1>", self.forgot_password)
        
        # Add bottom logo
        self.add_bottom_logo()
        
        # Set initial focus
        self.username_entry.focus()
    
    def add_bottom_logo(self):
        logo_path = os.path.join("assets", "loginlogo.png")
        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                logo_label = tk.Label(
                    self,
                    image=photo,
                    bg="#FFB6C1"
                )
                logo_label.image = photo
                logo_label.pack(side="bottom", pady=20)
            except Exception as e:
                print(f"Error loading bottom logo: {e}")
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        is_valid, error_message = validate_credentials(self.credentials, username, password)
        
        if is_valid:
            if self.login_success_callback:
                self.login_success_callback()
        else:
            messagebox.showerror("Error", error_message)
    
    def forgot_password(self, event):
        messagebox.showinfo("Forgot Password", "Coming soon")