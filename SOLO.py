"""
Combined application with all functionality in a single file.
"""
import tkinter as tk
import logging
import os
import threading
import cv2
from datetime import datetime, date, timedelta
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CREDENTIALS = {
    "1": "1",
    "user": "1"
}
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 680
SPLASH_DURATION = 3000
PINK_BUTTON = "#E75480"
LIGHT_CREAM = "#FFF5E1"
DARK_TEXT = "#333333"

# Utility Functions
def validate_credentials(credentials, username, password):
    """Validate user credentials"""
    if not username or not password:
        return False, "Username and password are required"
    
    if username not in credentials:
        logging.info(f"Login attempt: Username '{username}' not found")
        return False, "Invalid credentials"
        
    if credentials[username] != password:
        logging.info(f"Login attempt: Invalid password for user '{username}'")
        return False, "Invalid credentials"
    
    logging.info(f"Login successful for user: {username}")
    return True, None

def validate_amount(amount_str):
    """Validate that amount is a valid number"""
    try:
        amount = float(amount_str)
        return True, amount
    except ValueError:
        return False, "Amount must be a valid number"

def center_window(window, width, height):
    """Center a window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Account Data Model
class AccountData:
    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, amount: float, category: str, description: str, date=None):
        """Add a new transaction"""
        self.transactions.append({
            'amount': amount,
            'category': category,
            'description': description,
            'date': date or datetime.now()
        })
    
    @property
    def today_date(self):
        """Get formatted current date"""
        return datetime.now().strftime("%B %d, %Y")
    
    @property
    def income(self):
        """Calculate total income"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Income')
    
    @property
    def paid(self):
        """Calculate total paid amount"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Paid')
    
    @property
    def total_saving(self):
        """Calculate total savings"""
        return self.income - self.paid
    
    @property
    def monthly_range(self):
        """Get current month range"""
        today = date.today()
        first_day = date(today.year, today.month, 1)
        if today.month == 12:
            next_month = date(today.year + 1, 1, 1)
        else:
            next_month = date(today.year, today.month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        return f"{today.month}/1 - {today.month}/{last_day}"
    
    @property
    def monthly_transactions(self):
        """Get transactions for current month"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        return [t for t in self.transactions 
                if t['date'].month == current_month 
                and t['date'].year == current_year]
    
    @property
    def monthly_total(self):
        """Calculate total for current month"""
        monthly = self.monthly_transactions
        income = sum(t['amount'] for t in monthly if t['category'] == 'Income')
        paid = sum(t['amount'] for t in monthly if t['category'] == 'Paid')
        return income - paid

# Custom Toggle Button Component
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
            font=("Times new roman", 12, "bold"),
            **kwargs
        )
        
        self._variable = variable
        self.active_bg = "#E75480"
        self.active_fg = "white"
        self.inactive_bg = "white"
        self.inactive_fg = "black"
        self.hover_bg = "#E75480"
        
        self.configure(
            bg=self.inactive_bg,
            fg=self.inactive_fg,
            activebackground=self.active_bg,
            activeforeground=self.active_fg,
            selectcolor=self.active_bg
        )
        
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)
        
        self.update_state()
        self._variable.trace_add('write', lambda *args: self.update_state())
    
    def update_state(self):
        is_selected = self._variable.get() == self['value']
        self.configure(
            bg=self.active_bg if is_selected else self.inactive_bg,
            fg=self.active_fg if is_selected else self.inactive_fg
        )
    
    def on_hover(self, event):
        if self._variable.get() != self['value']:
            self.configure(bg=self.hover_bg, fg=self.active_fg)
    
    def on_leave(self, event):
        if self._variable.get() != self['value']:
            self.configure(bg=self.inactive_bg, fg=self.inactive_fg)

# View Classes
class SplashScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.is_playing = False
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        os.makedirs("assets", exist_ok=True)
        self.create_video_player()
        
    def create_video_player(self):
        self.video_path = os.path.join("assets", "gif.mp4")
        
        if os.path.exists(self.video_path):
            try:
                self.video_label = tk.Label(self, bg="#FFB6C1")
                self.video_label.pack(expand=True)
                
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
        try:
            cap = cv2.VideoCapture(self.video_path)
            
            while self.is_playing:
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image = self.resize_image(image, (self.winfo_width(), self.winfo_height()))
                photo = ImageTk.PhotoImage(image=image)
                
                self.video_label.configure(image=photo)
                self.video_label.image = photo
                
                cv2.waitKey(33)
            
            cap.release()
            
        except Exception as e:
            print(f"Error playing video: {e}")
            self.show_fallback_text()
    
    def resize_image(self, image, size):
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
        for widget in self.winfo_children():
            widget.destroy()
            
        label = tk.Label(
            self,
            text="webabiq",
            font=("Times new roman", 24, "bold"),
            bg="#FFB6C1",
            fg="#FF69B4"
        )
        label.pack(expand=True)
    
    def destroy(self):
        self.is_playing = False
        if hasattr(self, 'video_thread'):
            self.video_thread.join(timeout=1.0)
        super().destroy()

class LoginScreen(tk.Frame):
    def __init__(self, parent, credentials):
        super().__init__(parent)
        self.parent = parent
        self.credentials = credentials
        self.login_success_callback = None
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.login_container = tk.Frame(self, bg="white", highlightthickness=0)
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(
            self.login_container,
            text="webabiq",
            font=("Times new roman", 24, "bold"),
            bg="white",
            fg="#E75480"
        )
        title.pack(pady=(20, 30))
        
        tk.Label(
            self.login_container,
            text="USERNAME",
            font=("Times new roman", 12),
            bg="white",
            fg="#E75480"
        ).pack(anchor="w", padx=20)
        
        self.username_entry = tk.Entry(
            self.login_container,
            font=("Times new roman", 12),
            bg="#FFE4E1",
            relief="flat",
            width=30
        )
        self.username_entry.pack(padx=20, pady=(0, 20), ipady=8)
        
        tk.Label(
            self.login_container,
            text="PASSWORD",
            font=("Times new roman", 12),
            bg="white",
            fg="#E75480"
        ).pack(anchor="w", padx=20)
        
        self.password_entry = tk.Entry(
            self.login_container,
            font=("Times new roman", 12),
            bg="#FFE4E1",
            relief="flat",
            width=30,
            show="•"
        )
        self.password_entry.pack(padx=20, pady=(0, 20), ipady=8)
        
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        tk.Button(
            self.login_container,
            text="LOG IN",
            command=self.login,
            bg="#E75480",
            fg="white",
            font=("Times new roman", 12, "bold"),
            relief="flat",
            width=25,
            cursor="hand2"
        ).pack(pady=(0, 20), ipady=8)
        
        self.add_bottom_logo()
        self.username_entry.focus()
    
    def add_bottom_logo(self):
        logo_path = os.path.join("assets", "loginlogo.png")
        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                logo_label = tk.Label(self, image=photo, bg="#FFB6C1")
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

class InputScreen(tk.Frame):
    def __init__(self, parent, account_data, on_complete=None, on_back=None):
        super().__init__(parent)
        self.parent = parent
        self.account_data = account_data
        self.on_complete = on_complete
        self.on_back = on_back
        
        self.setup_ui()
        self.pack(fill="both", expand=True)
    
    def setup_ui(self):
        self.configure(bg="#FFE5E5")
        
        header_frame = tk.Frame(self, bg="#FFE5E5")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=("Times new roman", 24),
            bg="#FFE5E5",
            fg="#E75480",
            bd=0,
            command=self.return_to_account,
            cursor="hand2"
        )
        back_button.pack(side="left")
        
        tk.Label(
            header_frame,
            text="Input",
            font=("Times new roman", 24, "bold"),
            bg="#FFE5E5",
            fg="#E75480"
        ).pack(side="left", padx=20)
        
        type_frame = tk.Frame(self, bg="white", bd=0)
        type_frame.pack(fill="x", padx=20, pady=10)
        
        self.transaction_type = tk.StringVar(value="Income")
        
        self.paid_button = ToggleButton(
            type_frame,
            text="PAID",
            value="Paid",
            variable=self.transaction_type
        )
        self.paid_button.pack(side="left", expand=True)
        
        self.income_button = ToggleButton(
            type_frame,
            text="INCOME",
            value="Income",
            variable=self.transaction_type
        )
        self.income_button.pack(side="right", expand=True)
        
        date_frame = tk.Frame(self, bg="#E75480", bd=0)
        date_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            date_frame,
            text="DATE",
            font=("Times new roman", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=20, pady=15)
        
        self.date_entry = tk.Entry(
            date_frame,
            font=("Times new roman", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0
        )
        self.date_entry.pack(side="right", padx=20, pady=15, fill="x", expand=True)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        amount_frame = tk.Frame(self, bg="#E75480", bd=0)
        amount_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            amount_frame,
            text="AMOUNT",
            font=("Times new roman", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=20, pady=15)
        
        self.amount_entry = tk.Entry(
            amount_frame,
            font=("Times new roman", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0
        )
        self.amount_entry.pack(side="right", padx=20, pady=15, fill="x", expand=True)
        
        description_frame = tk.Frame(self, bg="#E75480", bd=0)
        description_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            description_frame,
            text="DESCRIPTION",
            font=("Times new roman", 14, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.description_text = tk.Text(
            description_frame,
            font=("Times new roman", 14),
            bg="#FFE4E1",
            fg="#666666",
            bd=0,
            height=8
        )
        self.description_text.pack(padx=20, pady=(5, 15), fill="both")
        
        tk.Button(
            self,
            text="SAVE",
            command=self.save_transaction,
            bg="#E75480",
            fg="white",
            font=("Times new roman", 14, "bold"),
            bd=0,
            pady=10,
            cursor="hand2"
        ).pack(side="bottom", fill="x", padx=20, pady=20)
    
    def save_transaction(self):
        amount_str = self.amount_entry.get().strip()
        is_valid, amount = validate_amount(amount_str)
        
        if not is_valid:
            messagebox.showerror("Error", amount)
            return
        
        description = self.description_text.get("1.0", "end-1c").strip()
        if not description:
            messagebox.showerror("Error", "Description is required")
            return
        
        try:
            date_str = self.date_entry.get()
            transaction_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        
        self.account_data.add_transaction(
            amount=amount,
            category=self.transaction_type.get(),
            description=description,
            date=transaction_date
        )
        
        self.pack_forget()
        if self.on_complete:
            self.on_complete()
    
    def return_to_account(self):
        self.pack_forget()
        if self.on_back:
            self.on_back()

class AccountScreen(tk.Frame):
    def __init__(self, parent, account_data):
        super().__init__(parent)
        self.parent = parent
        self.account_data = account_data
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.create_widgets()
        self.update_displays()
    
    def create_widgets(self):
        tk.Label(
            self,
            text="Account Book",
            font=("Times new roman", 32, "bold"),
            bg="#FFB6C1",
            fg="#E75480"
        ).pack(pady=(20, 10))
        
        tk.Label(
            self,
            text=self.account_data.today_date,
            font=("Times new roman", 14),
            bg="#FFB6C1",
            fg="#666666"
        ).pack(pady=(0, 20))
        
        month_frame = tk.Frame(self, bg="white", padx=30, pady=15)
        month_frame.pack(fill="x", padx=20)
        
        tk.Label(
            month_frame,
            text="THIS MONTH",
            font=("Times new roman", 16, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(side="left")
        
        self.saving_label = tk.Label(
            month_frame,
            text=f"${self.account_data.total_saving:.2f}",
            font=("Times new roman", 16, "bold"),
            bg="white",
            fg="#E75480"
        )
        self.saving_label.pack(side="right")
        
        buttons_frame = tk.Frame(self, bg="#FFB6C1")
        buttons_frame.pack(pady=20)
        
        income_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
        income_frame.pack(side="left", padx=10)
        
        tk.Label(
            income_frame,
            text="INCOME",
            font=("Times new roman", 12, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=5)
        
        self.income_label = tk.Label(
            income_frame,
            text=f"${self.account_data.income:.2f}",
            font=("Times new roman", 12, "bold"),
            bg="#E75480",
            fg="white"
        )
        self.income_label.pack(side="right", padx=5)
        
        paid_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
        paid_frame.pack(side="left", padx=10)
        
        tk.Label(
            paid_frame,
            text="PAID",
            font=("Times new roman", 12, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=5)
        
        self.paid_label = tk.Label(
            paid_frame,
            text=f"${self.account_data.paid:.2f}",
            font=("Times new roman", 12, "bold"),
            bg="#E75480",
            fg="white"
        )
        self.paid_label.pack(side="right", padx=5)
        
        tk.Button(
            self,
            text="Enter!",
            font=("Times new roman", 16, "bold"),
            bg="#FFE4E1",
            fg="#E75480",
            relief="flat",
            padx=40,
            pady=10,
            command=self.show_entry_dialog,
            cursor="hand2"
        ).pack(pady=20)
        
        monthly_frame = tk.Frame(self, bg="#E75480")
        monthly_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            monthly_frame,
            text=str(datetime.now().year),
            font=("Times new roman", 14, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(fill="x", pady=5)
        
        month_info_frame = tk.Frame(monthly_frame, bg="#E75480")
        month_info_frame.pack(fill="x", pady=5)
        
        self.monthly_range_label = tk.Label(
            month_info_frame,
            text=self.account_data.monthly_range,
            font=("Times new roman", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_range_label.pack(side="left", padx=20)
        
        self.monthly_amount_label = tk.Label(
            month_info_frame,
            text=f"${self.account_data.monthly_total:.2f}",
            font=("Times new roman", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_amount_label.pack(side="right", padx=20)
        
        self.list_container = tk.Frame(self, bg="white")
        self.list_container.pack(fill="both", expand=True, padx=20)
        
        headers_frame = tk.Frame(self.list_container, bg="#E75480")
        headers_frame.pack(fill="x", pady=(0, 1))
        
        self.columns = {
            "DATE": {"width": 12, "anchor": "center"},
            "AMOUNT": {"width": 12, "anchor": "center"},
            "DESCRIPTION": {"width": 40, "anchor": "w"}
        }
        
        for header, config in self.columns.items():
            tk.Label(
                headers_frame,
                text=header,
                font=("Times new roman", 10, "bold"),
                bg="#E75480",
                fg="white",
                width=config["width"],
                anchor=config["anchor"]
            ).pack(side="left", padx=5, pady=5)
        
        self.transactions_canvas = tk.Canvas(
            self.list_container,
            bg="white",
            highlightthickness=0
        )
        self.transactions_canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.transactions_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")
        
        self.transactions_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.transactions_frame = tk.Frame(self.transactions_canvas, bg="white")
        self.transactions_canvas.create_window(
            (0, 0),
            window=self.transactions_frame,
            anchor="nw",
            width=self.transactions_canvas.winfo_reqwidth()
        )
        
        self.transactions_frame.bind("<Configure>", self.on_frame_configure)
        self.transactions_canvas.bind("<Configure>", self.on_canvas_configure)
    
    def on_frame_configure(self, event=None):
        self.transactions_canvas.configure(scrollregion=self.transactions_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        self.transactions_canvas.itemconfig(
            self.transactions_canvas.find_withtag("all")[0],
            width=event.width
        )
    
    def show_entry_dialog(self):
        self.pack_forget()
        input_screen = InputScreen(
            self.parent,
            self.account_data,
            on_complete=self.on_input_complete,
            on_back=self.on_input_back
        )
    
    def on_input_complete(self):
        self.update_displays()
        self.pack(fill="both", expand=True)
    
    def on_input_back(self):
        self.pack(fill="both", expand=True)
    
    def update_displays(self):
        self.saving_label.config(text=f"${self.account_data.total_saving:.2f}")
        self.income_label.config(text=f"${self.account_data.income:.2f}")
        self.paid_label.config(text=f"${self.account_data.paid:.2f}")
        self.monthly_amount_label.config(text=f"${self.account_data.monthly_total:.2f}")
        
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        
        for transaction in reversed(self.account_data.monthly_transactions):
            row = tk.Frame(self.transactions_frame, bg="white")
            row.pack(fill="x", pady=1)
            
            tk.Label(
                row,
                text=transaction['date'].strftime("%Y-%m-%d"),
                bg="white",
                width=self.columns["DATE"]["width"],
                anchor=self.columns["DATE"]["anchor"]
            ).pack(side="left", padx=5)
            
            sign = "+" if transaction['category'] == "Income" else "-"
            amount_text = f"{sign}${transaction['amount']:.2f}"
            tk.Label(
                row,
                text=amount_text,
                bg="white",
                width=self.columns["AMOUNT"]["width"],
                anchor=self.columns["AMOUNT"]["anchor"],
                fg="#E75480" if sign == "+" else "#666666"
            ).pack(side="left", padx=5)
            
            description_label = tk.Label(
                row,
                text=transaction['description'],
                bg="white",
                anchor=self.columns["DESCRIPTION"]["anchor"],
                justify="left",
                wraplength=140
            )
            description_label.pack(side="left", padx=5, fill="x", expand=True)
        
        self.on_frame_configure()

def main():
    root = tk.Tk()
    root.title("Webabiq")
    
    os.makedirs("assets", exist_ok=True)
    center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    account_data = AccountData()
    splash = SplashScreen(root)
    
    def show_login():
        splash.destroy()
        login_screen = LoginScreen(root, CREDENTIALS)
        login_screen.login_success_callback = lambda: show_account(login_screen)
    
    def show_account(login_screen):
        login_screen.destroy()
        AccountScreen(root, account_data)
    
    root.after(SPLASH_DURATION, show_login)
    root.mainloop()

    from tkinter import PhotoImage
    icon = PhotoImage("assets", "webabiqlogo.png")
    root.iconphoto(True, icon)


if __name__ == "__main__":
    main()