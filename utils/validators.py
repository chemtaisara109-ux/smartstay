"""
Validation helper functions
"""
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    if not email:
        return False

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False

    return True

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False

    if len(password) < 8:
        return False

    # Check for at least one uppercase, one lowercase, one digit
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False

    return True

def validate_username(username):
    """Validate username"""
    if not username:
        return False

    if len(username) < 3 or len(username) > 50:
        return False

    # Alphanumeric, underscore, no spaces
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False

    return True

def validate_name(name):
    """Validate full name"""
    if not name:
        return False, "Full name is required"

    if len(name) < 2:
        return False, "Full name must be at least 2 characters long"

    if len(name) > 100:
        return False, "Full name must be less than 100 characters"

    # Check for valid characters (letters, spaces, apostrophes, hyphens)
    if not re.match(r"^[a-zA-Z\s'-]+$", name):
        return False, "Full name can only contain letters, spaces, apostrophes, and hyphens"

    return True, None

def validate_dates(check_in, check_out):
    """Validate booking dates"""
    if not check_in or not check_out:
        return False, "Check-in and check-out dates are required"

    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
    except ValueError:
        return False, "Invalid date format"

    if check_in_date >= check_out_date:
        return False, "Check-out must be after check-in"

    if check_in_date < datetime.now().date():
        return False, "Check-in date cannot be in the past"

    return True, None

def validate_guests(guests, max_guests):
    """Validate number of guests"""
    if not guests or guests < 1:
        return False, "Number of guests must be at least 1"

    if max_guests and guests > max_guests:
        return False, f"Maximum {max_guests} guests allowed for this property"

    return True, None