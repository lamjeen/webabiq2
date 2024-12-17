"""
Main application entry point.
"""
import tkinter as tk
import logging
from src.constants import (
    CREDENTIALS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SPLASH_DURATION
)
from src.utils.ui import center_window
from src.models.account import AccountData
from src.views.splash import SplashScreen
from src.views.login import LoginScreen
from src.views.account import AccountScreen

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    root = tk.Tk()
    root.title("Webabiq")
    
    # Center the window
    center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Create account data instance
    account_data = AccountData()
    
    # Create splash screen
    splash = SplashScreen(root)
    
    def show_login():
        splash.destroy()
        login_screen = LoginScreen(root, CREDENTIALS)
        login_screen.login_success_callback = lambda: show_account(login_screen)
    
    def show_account(login_screen):
        login_screen.destroy()
        AccountScreen(root, account_data)
    
    # Show login after splash duration
    root.after(SPLASH_DURATION, show_login)
    root.mainloop()

if __name__ == "__main__":
    main()