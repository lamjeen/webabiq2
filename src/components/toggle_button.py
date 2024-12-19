"""
Custom toggle button component.
"""
import tkinter as tk

class ToggleButton(tk.Radiobutton):
    def __init__(self, parent, text, value, variable, **kwargs):
        super().__init__(
            parent,
            text=text,
            value=value,
            variable=variable,
            indicatoron=False,
            width=15,
            pady=10,
            relief="flat",
            highlightthickness=0,
            font=("Arial", 12, "bold"),
            **kwargs
        )
        
        # Store variable reference and initial colors
        self._variable = variable
        self.active_bg = "#E75480"  # Pink background for selected state
        self.active_fg = "white"    # White text for selected state
        self.inactive_bg = "white"  # White background for unselected state
        self.inactive_fg = "black"  # Black text for unselected state
        self.hover_bg = "#E75480"   # Pink background for hover state
        
        # Configure initial state
        self.configure(
            bg=self.inactive_bg,
            fg=self.inactive_fg,
            activebackground=self.active_bg,
            activeforeground=self.active_fg,
            selectcolor=self.active_bg
        )
        
        # Bind events
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)
        
        # Update initial state
        self.update_state()
        self._variable.trace_add('write', lambda *args: self.update_state())
    
    def update_state(self):
        """Update button appearance based on selection state"""
        is_selected = self._variable.get() == self['value']
        self.configure(
            bg=self.active_bg if is_selected else self.inactive_bg,
            fg=self.active_fg if is_selected else self.inactive_fg
        )
    
    def on_hover(self, event):
        """Handle mouse hover"""
        if self._variable.get() != self['value']:
            self.configure(
                bg=self.hover_bg,
                fg=self.active_fg
            )
    
    def on_leave(self, event):
        """Handle mouse leave"""
        if self._variable.get() != self['value']:
            self.configure(
                bg=self.inactive_bg,
                fg=self.inactive_fg
            )