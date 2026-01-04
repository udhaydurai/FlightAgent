"""Price tracking utilities for flight alerts."""
from typing import Dict, Any, Optional
from api.utils.config import get_preferences


def should_send_alert(
    current_price: float,
    last_checked_price: Optional[float]
) -> bool:
    """
    Determine if an alert should be sent based on price drop.
    
    Alert Trigger: Only send emails if the price has dropped by >$10 
    compared to the last database entry.
    
    Args:
        current_price: Current flight price
        last_checked_price: Previous price from database (None if first check)
    
    Returns:
        True if alert should be sent, False otherwise
    """
    if last_checked_price is None:
        return False  # No previous price to compare
    
    prefs = get_preferences()
    threshold = prefs.get("alert_price_drop_threshold", 10.0)
    
    price_drop = last_checked_price - current_price
    
    return price_drop > threshold


def calculate_price_drop(
    current_price: float,
    last_checked_price: Optional[float]
) -> Optional[float]:
    """
    Calculate the price drop amount.
    
    Args:
        current_price: Current flight price
        last_checked_price: Previous price from database
    
    Returns:
        Price drop amount (positive if price decreased) or None if no previous price
    """
    if last_checked_price is None:
        return None
    
    return last_checked_price - current_price
