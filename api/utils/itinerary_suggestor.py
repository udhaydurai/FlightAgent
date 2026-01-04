"""Itinerary suggestion utilities."""
from typing import Dict, Any
from api.utils.config import get_preferences, get_dates


def suggest_itinerary_split(flight_found: bool = True) -> Dict[str, Any]:
    """
    Suggest a 3-day split between DC and NYC if a flight is found.
    
    Args:
        flight_found: Whether a suitable flight was found
    
    Returns:
        Dictionary with suggested itinerary split
    """
    if not flight_found:
        return {
            "suggested": False,
            "message": "No suitable flights found"
        }
    
    prefs = get_preferences()
    split_days = prefs.get("itinerary_split_days", 3)
    dates = get_dates()
    trip_duration = dates.get("trip_duration_days", 6)
    
    # Calculate split (default 3 days each for 6-day trip)
    dc_days = split_days
    nyc_days = trip_duration - split_days
    
    return {
        "suggested": True,
        "split": {
            "washington_dc": dc_days,
            "new_york": nyc_days
        },
        "total_days": trip_duration,
        "suggestions": {
            "washington_dc": [
                "Visit National Mall and monuments",
                "Explore Smithsonian museums",
                "Check out Cherry Blossom Festival (if in season)"
            ],
            "new_york": [
                "Visit Central Park",
                "Explore Times Square",
                "See Broadway shows",
                "Visit museums (MoMA, Met)"
            ]
        }
    }
