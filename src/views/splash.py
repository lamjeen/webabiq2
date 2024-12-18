"""
Splash screen view.
"""
import tkinter as tk
from PIL import Image, ImageTk
import os

class SplashScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configure pink background
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        # Create assets directory if it doesn't exist
        os.makedirs("assets", exist_ok=True)
        
        # Bind resize event
        self.bind('<Configure>', self.on_resize)
        
        # Create and display the logo
        self.create_logo()
    
    def create_logo(self):
        self.logo_path = os.path.join("assets", "gif.MOV")
        
        if os.path.exists(self.logo_path):
            try:
                # Load original image
                self.original_image = Image.open(self.logo_path)
                self.update_logo_size()
            except Exception as e:
                print(f"Error loading image: {e}")
                self.show_fallback_text()
        else:
            print(f"Logo file not found at: {self.logo_path}")
            self.show_fallback_text()
    
    def update_logo_size(self):
        try:
            # Get current frame size
            frame_width = self.winfo_width()
            frame_height = self.winfo_height()
            
            if frame_width > 1 and frame_height > 1:  # Ensure valid dimensions
                # Resize image to fill frame
                resized_image = self.resize_image(self.original_image, (frame_width, frame_height))
                photo = ImageTk.PhotoImage(resized_image)
                
                # Remove old label if exists
                for widget in self.winfo_children():
                    widget.destroy()
                
                # Create new label with updated image
                logo_label = tk.Label(self, image=photo, bg="#FFB6C1")
                logo_label.image = photo  # Keep a reference!
                logo_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error updating logo size: {e}")
            self.show_fallback_text()
    
    def on_resize(self, event):
        """Handle window resize events"""
        if hasattr(self, 'original_image'):
            self.update_logo_size()
    
    def resize_image(self, image, size):
        """Resize image to fill frame while maintaining aspect ratio"""
        target_width, target_height = size
        original_width, original_height = image.size
        
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        ratio = max(width_ratio, height_ratio)
        
        new_size = (int(original_width * ratio), int(original_height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def show_fallback_text(self):
        """Show fallback text when image cannot be loaded"""
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