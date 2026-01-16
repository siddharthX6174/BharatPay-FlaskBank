import re
from markupsafe import escape

def sanitize_string(value: str, max_length: int = 200) -> str:
    """Sanitize and escape user input."""
    if not value:
        return ""
    # Strip whitespace, escape HTML, limit length
    return escape(value.strip()[:max_length])

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_card_number(card_number: str) -> bool:
    """Validate 16-digit card number."""
    # Remove any spaces or dashes
    clean_number = re.sub(r'[\s-]', '', card_number)
    return bool(re.match(r'^\d{16}$', clean_number))

def validate_amount(amount: float) -> tuple[bool, str]:
    """Validate transaction amount."""
    if amount <= 0:
        return False, "Amount must be greater than zero"
    if amount > 10000000:  # 10 million limit
        return False, "Amount exceeds maximum limit"
    return True, ""

def clean_card_number(card_number: str) -> str:
    """Remove formatting from card number."""
    return re.sub(r'[\s-]', '', card_number)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets security requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains number
    - Contains special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain an uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain a lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain a special character"
    
    return True, ""
