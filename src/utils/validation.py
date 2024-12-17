"""
Input validation utilities.
"""

def validate_amount(amount_str):
    """Validate that amount is a valid number"""
    try:
        amount = float(amount_str)
        return True, amount
    except ValueError:
        return False, "Amount must be a valid number"