"""
Authentication utilities.
"""
import logging

def validate_credentials(credentials, username, password):
    """
    Validate user credentials
    Returns tuple (is_valid, error_message)
    """
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