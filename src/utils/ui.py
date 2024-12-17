"""
UI utility functions.
"""
import tkinter as tk

def create_gradient_background(widget, color1, color2):
    """Create a gradient background effect"""
    widget.configure(bg=color1)
    
    def gradient(width, height, color1, color2):
        canvas = tk.Canvas(widget, width=width, height=height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        for i in range(height):
            r1, g1, b1 = widget.winfo_rgb(color1)
            r2, g2, b2 = widget.winfo_rgb(color2)
            
            r = (r1 + int((r2-r1) * i/height))/256
            g = (g1 + int((g2-g1) * i/height))/256
            b = (b1 + int((b2-b1) * i/height))/256
            
            color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
            canvas.create_line(0, i, width, i, fill=color)
        
        return canvas
    
    widget.update()
    return gradient(widget.winfo_width(), widget.winfo_height(), color1, color2)

def center_window(window, width, height):
    """Center a window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")