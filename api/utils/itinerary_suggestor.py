"""Itinerary suggestion utilities."""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from api.utils.config import get_preferences, get_dates, get_open_jaw_config
from api.database import TravelTrackerDB


def get_cherry_blossom_info(year: int = 2026) -> Dict[str, Any]:
    """
    Get Cherry Blossom Festival peak bloom dates for Washington DC.
    
    The National Cherry Blossom Festival typically runs late March to mid-April.
    Peak bloom is usually around late March to early April.
    
    Args:
        year: Year to check (default 2026)
    
    Returns:
        Dictionary with festival dates and peak bloom info
    """
    # Historical peak bloom dates (approximate):
    # 2024: March 17
    # 2025: March 23 (predicted)
    # 2026: Typically late March to early April
    
    # Estimated peak bloom for 2026: March 25 - April 5
    peak_bloom_start = datetime(year, 3, 25)
    peak_bloom_end = datetime(year, 4, 5)
    festival_start = datetime(year, 3, 20)
    festival_end = datetime(year, 4, 14)
    
    return {
        "festival_start": festival_start.strftime("%Y-%m-%d"),
        "festival_end": festival_end.strftime("%Y-%m-%d"),
        "peak_bloom_start": peak_bloom_start.strftime("%Y-%m-%d"),
        "peak_bloom_end": peak_bloom_end.strftime("%Y-%m-%d"),
        "festival_name": "National Cherry Blossom Festival",
        "location": "Washington, D.C.",
        "website": "https://nationalcherryblossomfestival.org/"
    }


def check_cherry_blossom_overlap(departure_date: str, return_date: str) -> Dict[str, Any]:
    """
    Check if trip dates overlap with Cherry Blossom Festival peak bloom.
    
    Args:
        departure_date: Trip departure date (YYYY-MM-DD)
        return_date: Trip return date (YYYY-MM-DD)
    
    Returns:
        Dictionary with overlap information
    """
    try:
        dep = datetime.strptime(departure_date, "%Y-%m-%d")
        ret = datetime.strptime(return_date, "%Y-%m-%d")
        year = dep.year
        
        cherry_info = get_cherry_blossom_info(year)
        peak_start = datetime.strptime(cherry_info["peak_bloom_start"], "%Y-%m-%d")
        peak_end = datetime.strptime(cherry_info["peak_bloom_end"], "%Y-%m-%d")
        festival_start = datetime.strptime(cherry_info["festival_start"], "%Y-%m-%d")
        festival_end = datetime.strptime(cherry_info["festival_end"], "%Y-%m-%d")
        
        # Check if trip overlaps with peak bloom
        overlaps_peak = (dep <= peak_end) and (ret >= peak_start)
        
        # Check if trip overlaps with festival period
        overlaps_festival = (dep <= festival_end) and (ret >= festival_start)
        
        # Calculate days in DC during peak bloom (if visiting DC first)
        dc_days_during_peak = 0
        if overlaps_peak:
            # Estimate 3 days in DC (can be adjusted based on actual itinerary)
            dc_start = dep
            dc_end = dep + timedelta(days=3)
            peak_overlap_start = max(dc_start, peak_start)
            peak_overlap_end = min(dc_end, peak_end)
            if peak_overlap_start <= peak_overlap_end:
                dc_days_during_peak = (peak_overlap_end - peak_overlap_start).days + 1
        
        return {
            "overlaps_peak_bloom": overlaps_peak,
            "overlaps_festival": overlaps_festival,
            "festival_info": cherry_info,
            "dc_days_during_peak": dc_days_during_peak,
            "recommendation": "Visit DC during peak bloom!" if overlaps_peak else "Consider adjusting dates to catch peak bloom"
        }
    except Exception as e:
        return {
            "overlaps_peak_bloom": False,
            "overlaps_festival": False,
            "error": str(e)
        }


def analyze_best_routing(db: Optional[TravelTrackerDB] = None) -> Dict[str, Any]:
    """
    Analyze best flight routing options from database to suggest optimal itinerary.
    
    Compares prices for:
    - Option 1: SAN → DC / NYC → SAN
    - Option 2: SAN → NYC / DC → SAN
    
    Args:
        db: Database instance (creates new if None)
    
    Returns:
        Dictionary with routing analysis and recommendations
    """
    if db is None:
        db = TravelTrackerDB()
    
    # Get all recent best prices
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT departure_date, return_date, inbound_airport, outbound_airport,
                   total_price, currency, routing_description
            FROM flight_prices
            WHERE is_best_price = 1 OR total_price IN (
                SELECT MIN(total_price) FROM flight_prices
                GROUP BY departure_date, return_date
            )
            ORDER BY total_price ASC
            LIMIT 20
        """)
        records = [dict(row) for row in cursor.fetchall()]
    
    if not records:
        return {
            "success": False,
            "message": "No flight data found in database"
        }
    
    # Categorize by routing direction
    dc_first_routes = []  # SAN → DC / NYC → SAN
    nyc_first_routes = []  # SAN → NYC / DC → SAN
    
    for record in records:
        routing = record.get("routing_description", "").lower()
        if "san → dc" in routing or "san → washington" in routing:
            dc_first_routes.append(record)
        elif "san → nyc" in routing or "san → new york" in routing:
            nyc_first_routes.append(record)
    
    # Calculate averages
    dc_first_avg = sum(r["total_price"] for r in dc_first_routes) / len(dc_first_routes) if dc_first_routes else None
    nyc_first_avg = sum(r["total_price"] for r in nyc_first_routes) / len(nyc_first_routes) if nyc_first_routes else None
    
    # Find best option
    best_dc_first = min(dc_first_routes, key=lambda x: x["total_price"]) if dc_first_routes else None
    best_nyc_first = min(nyc_first_routes, key=lambda x: x["total_price"]) if nyc_first_routes else None
    
    # Determine recommendation
    if best_dc_first and best_nyc_first:
        if best_dc_first["total_price"] < best_nyc_first["total_price"]:
            recommended = "dc_first"
            savings = best_nyc_first["total_price"] - best_dc_first["total_price"]
        else:
            recommended = "nyc_first"
            savings = best_dc_first["total_price"] - best_nyc_first["total_price"]
    elif best_dc_first:
        recommended = "dc_first"
        savings = None
    elif best_nyc_first:
        recommended = "nyc_first"
        savings = None
    else:
        recommended = None
        savings = None
    
    return {
        "success": True,
        "dc_first_routes": {
            "count": len(dc_first_routes),
            "average_price": dc_first_avg,
            "best_option": best_dc_first
        },
        "nyc_first_routes": {
            "count": len(nyc_first_routes),
            "average_price": nyc_first_avg,
            "best_option": best_nyc_first
        },
        "recommended_routing": recommended,
        "estimated_savings": savings,
        "currency": records[0].get("currency", "USD") if records else "USD"
    }


def suggest_optimal_itinerary(
    departure_date: Optional[str] = None,
    return_date: Optional[str] = None,
    db: Optional[TravelTrackerDB] = None
) -> Dict[str, Any]:
    """
    Suggest optimal 6-day itinerary split based on cheapest flight direction and Cherry Blossom dates.
    
    Args:
        departure_date: Specific departure date to analyze (optional)
        return_date: Specific return date to analyze (optional)
        db: Database instance (optional)
    
    Returns:
        Dictionary with complete itinerary recommendation
    """
    dates = get_dates()
    prefs = get_preferences()
    trip_duration = dates.get("trip_duration_days", 6)
    default_split = prefs.get("itinerary_split_days", 3)
    
    # Analyze routing options
    routing_analysis = analyze_best_routing(db)
    
    if not routing_analysis.get("success"):
        return {
            "suggested": False,
            "message": "Insufficient flight data for recommendation"
        }
    
    # Determine which city to visit first
    recommended_routing = routing_analysis.get("recommended_routing")
    
    if recommended_routing == "dc_first":
        first_city = "washington_dc"
        second_city = "new_york"
        dc_days = default_split
        nyc_days = trip_duration - default_split
        routing_desc = "Fly SAN → DC, travel to NYC, fly NYC → SAN"
    elif recommended_routing == "nyc_first":
        first_city = "new_york"
        second_city = "washington_dc"
        nyc_days = default_split
        dc_days = trip_duration - default_split
        routing_desc = "Fly SAN → NYC, travel to DC, fly DC → SAN"
    else:
        # Default to DC first if unclear
        first_city = "washington_dc"
        second_city = "new_york"
        dc_days = default_split
        nyc_days = trip_duration - default_split
        routing_desc = "Fly SAN → DC, travel to NYC, fly NYC → SAN"
    
    # Check Cherry Blossom overlap if we have dates
    cherry_blossom_info = None
    if departure_date and return_date:
        cherry_blossom_info = check_cherry_blossom_overlap(departure_date, return_date)
        
        # Adjust split if Cherry Blossom peak bloom suggests visiting DC first
        if cherry_blossom_info.get("overlaps_peak_bloom") and first_city != "washington_dc":
            # Recommend DC first during peak bloom
            first_city = "washington_dc"
            second_city = "new_york"
            dc_days = default_split + 1  # Extra day for peak bloom
            nyc_days = trip_duration - dc_days
            routing_desc = "Fly SAN → DC (peak bloom!), travel to NYC, fly NYC → SAN"
    
    # Build suggestions
    dc_suggestions = [
        "Visit National Mall and monuments",
        "Explore Smithsonian museums (free admission)",
        "See the White House and Capitol Building",
        "Walk around Georgetown",
        "Visit Arlington National Cemetery"
    ]
    
    nyc_suggestions = [
        "Visit Central Park",
        "Explore Times Square",
        "See Broadway shows",
        "Visit museums (MoMA, Met, Natural History)",
        "Walk the High Line",
        "See Statue of Liberty and Ellis Island"
    ]
    
    # Add Cherry Blossom to DC suggestions if relevant
    if cherry_blossom_info and cherry_blossom_info.get("overlaps_peak_bloom"):
        dc_suggestions.insert(0, f"🌸 See Cherry Blossom Festival peak bloom! ({cherry_blossom_info['festival_info']['peak_bloom_start']} - {cherry_blossom_info['festival_info']['peak_bloom_end']})")
    
    return {
        "suggested": True,
        "routing_analysis": routing_analysis,
        "recommended_routing": routing_desc,
        "first_city": first_city,
        "second_city": second_city,
        "split": {
            "washington_dc": dc_days,
            "new_york": nyc_days
        },
        "total_days": trip_duration,
        "cherry_blossom_info": cherry_blossom_info,
        "suggestions": {
            "washington_dc": dc_suggestions,
            "new_york": nyc_suggestions
        },
        "estimated_savings": routing_analysis.get("estimated_savings")
    }


def suggest_itinerary_split(flight_found: bool = True) -> Dict[str, Any]:
    """
    Suggest a 3-day split between DC and NYC if a flight is found.
    (Legacy function for backward compatibility)
    
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
