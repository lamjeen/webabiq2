"""
Account data model and transaction management.
"""
from datetime import datetime, date, timedelta

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