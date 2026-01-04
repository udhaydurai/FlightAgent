"""Flight filtering utilities based on travel agent constraints."""
from typing import Dict, Any, List, Optional
from datetime import datetime, time
from api.utils.config import get_preferences, get_origin, get_destinations


def parse_time(time_str: str) -> Optional[time]:
    """Parse time from ISO format or HH:MM format."""
    try:
        if "T" in time_str:
            dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            return dt.time()
        else:
            return datetime.strptime(time_str, "%H:%M").time()
    except (ValueError, AttributeError):
        return None


def is_red_eye(flight_offer: Dict[str, Any]) -> bool:
    """
    Check if a flight is a red-eye based on roadmap constraints.
    
    Red-eye constraint: Exclude flights departing SAN before 7:00 AM 
    or arriving East Coast after 10:00 PM.
    
    Args:
        flight_offer: Flight offer dictionary from Amadeus API
    
    Returns:
        True if flight is a red-eye, False otherwise
    """
    prefs = get_preferences()
    no_red_eyes = prefs.get("no_red_eyes", True)
    
    if not no_red_eyes:
        return False
    
    origin_code = get_origin()  # SAN
    destinations = get_destinations()
    east_coast_airports = set(destinations.get("all_airports", []))
    
    itinerary = flight_offer.get("itineraries", [{}])[0]
    segments = itinerary.get("segments", [])
    
    if not segments:
        return False
    
    first_segment = segments[0]
    last_segment = segments[-1]
    
    departure_airport = first_segment.get("departure", {}).get("iataCode", "")
    departure_time_str = first_segment.get("departure", {}).get("at", "")
    
    arrival_airport = last_segment.get("arrival", {}).get("iataCode", "")
    arrival_time_str = last_segment.get("arrival", {}).get("at", "")
    
    # Check: Departing SAN before 7:00 AM
    if departure_airport == origin_code:
        departure_time = parse_time(departure_time_str)
        if departure_time:
            san_departure_cutoff = datetime.strptime(
                prefs.get("red_eye_departure_san_before", "07:00"), 
                "%H:%M"
            ).time()
            if departure_time < san_departure_cutoff:
                return True
    
    # Check: Arriving East Coast after 10:00 PM
    if arrival_airport in east_coast_airports:
        arrival_time = parse_time(arrival_time_str)
        if arrival_time:
            east_coast_arrival_cutoff = datetime.strptime(
                prefs.get("red_eye_arrival_east_coast_after", "22:00"), 
                "%H:%M"
            ).time()
            if arrival_time > east_coast_arrival_cutoff:
                return True
    
    return False


def is_was_nyc_route(flight_offer: Dict[str, Any]) -> bool:
    """
    Check if flight is between Washington D.C. and New York airports.
    
    Args:
        flight_offer: Flight offer dictionary from Amadeus API
    
    Returns:
        True if route is between WAS (IAD/DCA) and NYC (JFK/LGA/EWR)
    """
    was_airports = {"IAD", "DCA"}
    nyc_airports = {"JFK", "LGA", "EWR"}
    
    itinerary = flight_offer.get("itineraries", [{}])[0]
    segments = itinerary.get("segments", [])
    
    if not segments:
        return False
    
    first_segment = segments[0]
    last_segment = segments[-1]
    
    origin = first_segment.get("departure", {}).get("iataCode", "")
    destination = last_segment.get("arrival", {}).get("iataCode", "")
    
    # Check if origin is WAS and destination is NYC, or vice versa
    return (origin in was_airports and destination in nyc_airports) or \
           (origin in nyc_airports and destination in was_airports)


def has_too_many_stops(flight_offer: Dict[str, Any]) -> bool:
    """
    Check if flight has too many stops based on route type.
    
    Constraint: 
    - WAS-NYC routes: Only nonstop flights allowed
    - Other routes: Max 1 stop allowed
    
    Args:
        flight_offer: Flight offer dictionary from Amadeus API
    
    Returns:
        True if flight has too many stops, False otherwise
    """
    prefs = get_preferences()
    max_stops = prefs.get("max_stops", 0)  # Default to 0 (nonstop required)
    nonstop_required = prefs.get("nonstop_required", True)
    was_nyc_nonstop_only = prefs.get("was_nyc_nonstop_only", True)
    
    # Count segments in the itinerary
    itinerary = flight_offer.get("itineraries", [{}])[0]
    segments = itinerary.get("segments", [])
    
    # Number of stops = number of segments - 1
    num_stops = len(segments) - 1 if segments else 0
    
    # Special rule: WAS-NYC routes must be nonstop
    if was_nyc_nonstop_only and is_was_nyc_route(flight_offer):
        return num_stops > 0  # Reject any stops for WAS-NYC
    
    # If nonstop required, reject any stops
    if nonstop_required:
        return num_stops > 0
    
    return num_stops > max_stops


def filter_flights(flight_offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter flight offers based on travel agent constraints.
    
    Constraints applied:
    1. No red-eyes (exclude flights departing SAN before 7:00 AM or arriving East Coast after 10:00 PM)
    2. Nonstop required for all long-haul segments (max_stops: 0)
    3. WAS-NYC routes: Only nonstop flights allowed
    
    Args:
        flight_offers: List of flight offer dictionaries from Amadeus API
    
    Returns:
        Filtered list of flight offers
    """
    prefs = get_preferences()
    nonstop_required = prefs.get("nonstop_required", True)
    
    filtered = []
    
    for offer in flight_offers:
        # Check red-eye constraint (departing SAN before 7 AM or arriving East Coast after 10 PM)
        if is_red_eye(offer):
            continue  # Skip red-eye flights
        
        # Check stop constraint (nonstop required)
        if nonstop_required:
            if has_too_many_stops(offer):
                continue  # Skip flights with stops
        else:
            if has_too_many_stops(offer):
                continue  # Skip flights with >1 stop
        
        filtered.append(offer)
    
    return filtered


def sort_by_preference(flight_offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort flight offers by preference (nonstop first, then by duration).
    
    Args:
        flight_offers: List of flight offer dictionaries
    
    Returns:
        Sorted list of flight offers
    """
    def get_sort_key(offer: Dict[str, Any]) -> tuple:
        # Count stops (prefer fewer stops)
        itinerary = offer.get("itineraries", [{}])[0]
        segments = itinerary.get("segments", [])
        num_stops = len(segments) - 1 if segments else 0
        
        # Get duration in minutes
        duration = itinerary.get("duration", "")
        # Parse duration (e.g., "PT2H30M" -> 150 minutes)
        duration_minutes = parse_duration(duration)
        
        # Sort by: (stops, duration)
        return (num_stops, duration_minutes)
    
    return sorted(flight_offers, key=get_sort_key)


def parse_duration(duration_str: str) -> int:
    """
    Parse ISO 8601 duration string to minutes.
    
    Args:
        duration_str: Duration in ISO 8601 format (e.g., "PT2H30M")
    
    Returns:
        Duration in minutes
    """
    if not duration_str or not duration_str.startswith("PT"):
        return 0
    
    hours = 0
    minutes = 0
    
    # Extract hours
    if "H" in duration_str:
        h_idx = duration_str.index("H")
        hours = int(duration_str[2:h_idx])
        duration_str = duration_str[h_idx + 1:]
    
    # Extract minutes
    if "M" in duration_str:
        m_idx = duration_str.index("M")
        minutes = int(duration_str[:m_idx])
    
    return hours * 60 + minutes
