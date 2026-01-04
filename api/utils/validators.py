"""Input validation utilities for Flight Agent."""
import re
from datetime import datetime
from typing import Optional
from api.utils.errors import ValidationError


def validate_airport_code(code: str) -> str:
    """
    Validate airport IATA code.
    
    Args:
        code: Airport code to validate
    
    Returns:
        Uppercase airport code
    
    Raises:
        ValidationError: If code is invalid
    """
    if not code or not isinstance(code, str):
        raise ValidationError(f"Invalid airport code: {code}")
    
    code = code.upper().strip()
    
    if not re.match(r'^[A-Z]{3}$', code):
        raise ValidationError(f"Airport code must be 3 uppercase letters: {code}")
    
    return code


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> str:
    """
    Validate and normalize date string.
    
    Args:
        date_str: Date string to validate
        date_format: Expected date format (default: YYYY-MM-DD)
    
    Returns:
        Normalized date string
    
    Raises:
        ValidationError: If date is invalid
    """
    if not date_str or not isinstance(date_str, str):
        raise ValidationError(f"Invalid date: {date_str}")
    
    try:
        # Try to parse the date
        parsed_date = datetime.strptime(date_str.strip(), date_format)
        
        # Check if date is in the future (for departure dates)
        if parsed_date < datetime.now():
            raise ValidationError(f"Date must be in the future: {date_str}")
        
        return parsed_date.strftime(date_format)
    except ValueError as e:
        raise ValidationError(f"Invalid date format. Expected {date_format}: {date_str}") from e


def validate_passenger_count(count: int, min_count: int = 1, max_count: int = 9) -> int:
    """
    Validate passenger count.
    
    Args:
        count: Number of passengers
        min_count: Minimum allowed (default: 1)
        max_count: Maximum allowed (default: 9)
    
    Returns:
        Validated passenger count
    
    Raises:
        ValidationError: If count is invalid
    """
    if not isinstance(count, int):
        raise ValidationError(f"Passenger count must be an integer: {count}")
    
    if count < min_count or count > max_count:
        raise ValidationError(f"Passenger count must be between {min_count} and {max_count}: {count}")
    
    return count


def validate_price(price: Optional[float], min_price: float = 0) -> Optional[float]:
    """
    Validate price value.
    
    Args:
        price: Price to validate (can be None)
        min_price: Minimum allowed price (default: 0)
    
    Returns:
        Validated price or None
    
    Raises:
        ValidationError: If price is invalid
    """
    if price is None:
        return None
    
    if not isinstance(price, (int, float)):
        raise ValidationError(f"Price must be a number: {price}")
    
    if price < min_price:
        raise ValidationError(f"Price must be >= {min_price}: {price}")
    
    return float(price)
