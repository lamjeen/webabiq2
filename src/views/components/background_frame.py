"""
Background frame component with image support.
"""
import tkinter as tk
from PIL import Image, ImageTk
import os

class BackgroundFrame(tk.Frame):
    def __init__(self, parent, image_path, fallback_color="#FFE5E5"):
        super().__init__(parent)
        self.image_path = image_path
        self.fallback_color = fallback_color
        self.configure(bg=self.fallback_color)
        
        self.setup_background()
        self.bind('<Configure>', self.on_resize)
    
    def setup_background(self):
        """Setup the background image"""
        try:
            if os.path.exists(self.image_path):
                self.load_background_image()
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.configure(bg=self.fallback_color)
    
    def load_background_image(self):
        """Load and display the background image"""
        self.original_image = Image.open(self.image_path)
        self.update_background_image()
    
    def update_background_image(self):
        """Update background image with current dimensions"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:  # Get parent dimensions if not yet sized
            width = self.master.winfo_width()
            height = self.master.winfo_height()
        
        if width > 1 and height > 1:
            resized_image = self.original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            
            if not hasattr(self, 'bg_label'):
                self.bg_label = tk.Label(
                    self,
                    image=self.bg_photo,
                    borderwidth=0,
                    highlightthickness=0
                )
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                self.bg_label.configure(image=self.bg_photo)
    
    def on_resize(self, event):
        """Handle resize events"""
        if event.width > 1 and event.height > 1:
            self.update_background_image()