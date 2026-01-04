"""Utilities to extract flight details from Amadeus API responses."""
from typing import Dict, Any, Optional, List


def extract_flight_numbers(flight_data: Dict[str, Any]) -> str:
    """Extract flight numbers from flight offer."""
    if not flight_data:
        return ""
    
    flight_numbers = []
    itineraries = flight_data.get("itineraries", [])
    
    for itinerary in itineraries:
        segments = itinerary.get("segments", [])
        for segment in segments:
            carrier = segment.get("carrierCode", "")
            number = segment.get("number", "")
            if carrier and number:
                flight_numbers.append(f"{carrier}{number}")
    
    return ", ".join(flight_numbers)


def extract_airlines(flight_data: Dict[str, Any]) -> str:
    """Extract airline names from flight offer."""
    if not flight_data:
        return ""
    
    airlines = set()
    itineraries = flight_data.get("itineraries", [])
    dictionaries = flight_data.get("dictionaries", {})
    carriers = dictionaries.get("carriers", {})
    
    for itinerary in itineraries:
        segments = itinerary.get("segments", [])
        for segment in segments:
            carrier_code = segment.get("carrierCode", "")
            if carrier_code and carrier_code in carriers:
                airlines.add(carriers[carrier_code])
    
    return ", ".join(sorted(airlines))


def generate_booking_url(
    flight_offer: Dict[str, Any],
    base_url: str = "https://www.amadeus.com"
) -> Optional[str]:
    """
    Generate a booking URL for a flight offer.
    
    Note: Amadeus API doesn't provide direct booking URLs in the search response.
    You need to use Flight Offers Price API and Flight Create Order API to get
    actual booking links. This is a placeholder that could be enhanced.
    
    Args:
        flight_offer: Flight offer from Amadeus API
        base_url: Base URL for booking (placeholder)
    
    Returns:
        Booking URL string or None
    """
    # Placeholder - actual implementation would require:
    # 1. Flight Offers Price API call to confirm price
    # 2. Flight Create Order API call to create booking
    # 3. Get actual booking URL from order response
    
    # For now, return a generic search URL or None
    # In production, you'd integrate with Amadeus booking flow
    
    return None


def extract_flight_summary(flight_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key flight details for display."""
    if not flight_data:
        return {}
    
    summary = {
        "flight_numbers": extract_flight_numbers(flight_data),
        "airlines": extract_airlines(flight_data),
        "price": flight_data.get("price", {}).get("total", ""),
        "currency": flight_data.get("price", {}).get("currency", "USD")
    }
    
    # Extract departure/arrival times
    itineraries = flight_data.get("itineraries", [])
    if itineraries:
        itinerary = itineraries[0]
        segments = itinerary.get("segments", [])
        if segments:
            first_segment = segments[0]
            last_segment = segments[-1]
            
            summary["departure"] = {
                "airport": first_segment.get("departure", {}).get("iataCode", ""),
                "time": first_segment.get("departure", {}).get("at", "")
            }
            summary["arrival"] = {
                "airport": last_segment.get("arrival", {}).get("iataCode", ""),
                "time": last_segment.get("arrival", {}).get("at", "")
            }
            summary["duration"] = itinerary.get("duration", "")
    
    return summary
