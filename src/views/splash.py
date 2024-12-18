"""
Splash screen view with video support.
"""
import tkinter as tk
from tkinter import ttk
import os
import threading
import cv2
from PIL import Image, ImageTk

class SplashScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.is_playing = False
        
        # Configure pink background
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        # Create assets directory if it doesn't exist
        os.makedirs("assets", exist_ok=True)
        
        # Create and display the video
        self.create_video_player()
        
    def create_video_player(self):
        self.video_path = os.path.join("assets", "gif.mp4")
        
        if os.path.exists(self.video_path):
            try:
                # Create a label to display video frames
                self.video_label = tk.Label(self, bg="#FFB6C1")
                self.video_label.pack(expand=True)
                
                # Start video playback in a separate thread
                self.is_playing = True
                self.video_thread = threading.Thread(target=self.play_video)
                self.video_thread.daemon = True
                self.video_thread.start()
                
            except Exception as e:
                print(f"Error setting up video player: {e}")
                self.show_fallback_text()
        else:
            print(f"Video file not found at: {self.video_path}")
            self.show_fallback_text()
    
    def play_video(self):
        """Play the video file"""
        try:
            cap = cv2.VideoCapture(self.video_path)
            
            while self.is_playing:
                ret, frame = cap.read()
                if not ret:
                    # Reset to beginning of video when it ends
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Convert frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                image = Image.fromarray(frame_rgb)
                
                # Resize image to fit the window
                image = self.resize_image(image, (self.winfo_width(), self.winfo_height()))
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image=image)
                
                # Update label with new frame
                self.video_label.configure(image=photo)
                self.video_label.image = photo
                
                # Control frame rate
                cv2.waitKey(33)  # approximately 30 fps
            
            cap.release()
            
        except Exception as e:
            print(f"Error playing video: {e}")
            self.show_fallback_text()
    
    def resize_image(self, image, size):
        """Resize image to fill frame while maintaining aspect ratio"""
        target_width, target_height = size
        if target_width <= 1 or target_height <= 1:
            return image
            
        original_width, original_height = image.size
        
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        ratio = max(width_ratio, height_ratio)
        
        new_size = (int(original_width * ratio), int(original_height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def show_fallback_text(self):
        """Show fallback text when video cannot be loaded"""
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
    
    def destroy(self):
        """Clean up resources before destroying the widget"""
        self.is_playing = False
        if hasattr(self, 'video_thread'):
            self.video_thread.join(timeout=1.0)
        super().destroy()