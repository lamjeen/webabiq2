"""
Splash screen view.
"""
import tkinter as tk
from PIL import Image, ImageTk
import os
from src.constants import PINK_GRADIENT_START, PINK_GRADIENT_END

class SplashScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        self.create_logo()
    
    def create_logo(self):
        logo_path = os.path.join("assets", "logo.png")
        
        if os.path.exists(logo_path):
            try:
                self.original_image = Image.open(logo_path)
                self.update_logo_size()
            except Exception as e:
                print(f"Error loading image: {e}")
                self.show_fallback_text()
        else:
            self.show_fallback_text()
    
    def update_logo_size(self):
        try:
            frame_width = self.winfo_width()
            frame_height = self.winfo_height()
            
            if frame_width > 1 and frame_height > 1:
                resized_image = self.resize_image(self.original_image, (frame_width, frame_height))
                photo = ImageTk.PhotoImage(resized_image)
                
                for widget in self.winfo_children():
                    widget.destroy()
                
                logo_label = tk.Label(self, image=photo, bg="#FFB6C1")
                logo_label.image = photo
                logo_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error updating logo size: {e}")
            self.show_fallback_text()
    
    def resize_image(self, image, size):
        target_width, target_height = size
        original_width, original_height = image.size
        
        ratio = max(target_width / original_width, target_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def show_fallback_text(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        label = tk.Label(
            self,
            text="webabiq",
            font=("Arial", 24, "bold"),
            bg="#FFB6C1",
            fg="#FF69B4"
        )
        label.pack(expand=True)