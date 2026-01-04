"""Phase 5: Final Itinerary Recommendations."""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import TravelTrackerDB
from api.utils.config import get_dates, get_open_jaw_config
from api.utils.itinerary_suggestor import (
    suggest_optimal_itinerary,
    analyze_best_routing,
    check_cherry_blossom_overlap,
    get_cherry_blossom_info
)


def format_price(price: float, currency: str = "USD") -> str:
    """Format price for display."""
    return f"{currency} ${price:.2f}"


def display_routing_analysis(analysis: Dict[str, Any]):
    """Display routing analysis results."""
    print("\n" + "=" * 80)
    print("📊 FLIGHT ROUTING ANALYSIS")
    print("=" * 80)
    
    if not analysis.get("success"):
        print(f"❌ {analysis.get('message', 'Analysis failed')}")
        return
    
    dc_first = analysis.get("dc_first_routes", {})
    nyc_first = analysis.get("nyc_first_routes", {})
    currency = analysis.get("currency", "USD")
    
    print(f"\n✈️  Option 1: SAN → DC / NYC → SAN")
    print(f"   Routes found: {dc_first.get('count', 0)}")
    if dc_first.get("average_price"):
        print(f"   Average price: {format_price(dc_first['average_price'], currency)}")
    if dc_first.get("best_option"):
        best = dc_first["best_option"]
        print(f"   Best price: {format_price(best['total_price'], currency)}")
        print(f"   Dates: {best.get('departure_date')} → {best.get('return_date')}")
        print(f"   Airports: {best.get('inbound_airport')} / {best.get('outbound_airport')}")
    
    print(f"\n✈️  Option 2: SAN → NYC / DC → SAN")
    print(f"   Routes found: {nyc_first.get('count', 0)}")
    if nyc_first.get("average_price"):
        print(f"   Average price: {format_price(nyc_first['average_price'], currency)}")
    if nyc_first.get("best_option"):
        best = nyc_first["best_option"]
        print(f"   Best price: {format_price(best['total_price'], currency)}")
        print(f"   Dates: {best.get('departure_date')} → {best.get('return_date')}")
        print(f"   Airports: {best.get('inbound_airport')} / {best.get('outbound_airport')}")
    
    recommended = analysis.get("recommended_routing")
    if recommended:
        print(f"\n✅ RECOMMENDED: {'DC First' if recommended == 'dc_first' else 'NYC First'}")
        savings = analysis.get("estimated_savings")
        if savings:
            print(f"   Estimated savings: {format_price(savings, currency)}")


def display_cherry_blossom_info(departure_date: str, return_date: str):
    """Display Cherry Blossom Festival information."""
    print("\n" + "=" * 80)
    print("🌸 CHERRY BLOSSOM FESTIVAL CHECK")
    print("=" * 80)
    
    cherry_info = check_cherry_blossom_overlap(departure_date, return_date)
    festival_info = cherry_info.get("festival_info", {})
    
    if festival_info:
        print(f"\n📅 Festival Dates: {festival_info.get('festival_start')} to {festival_info.get('festival_end')}")
        print(f"🌸 Peak Bloom: {festival_info.get('peak_bloom_start')} to {festival_info.get('peak_bloom_end')}")
        print(f"📍 Location: {festival_info.get('location')}")
        print(f"🌐 Website: {festival_info.get('website')}")
    
    if cherry_info.get("overlaps_peak_bloom"):
        print(f"\n✅ GREAT NEWS! Your trip overlaps with peak bloom!")
        print(f"   Days in DC during peak: {cherry_info.get('dc_days_during_peak', 0)}")
        print(f"   💡 Recommendation: Visit DC first to catch the peak bloom!")
    elif cherry_info.get("overlaps_festival"):
        print(f"\n⚠️  Your trip overlaps with the festival period but not peak bloom.")
        print(f"   You may still see some blossoms, but peak bloom is earlier.")
    else:
        print(f"\n❌ Your trip dates don't overlap with peak bloom.")
        print(f"   Peak bloom: {festival_info.get('peak_bloom_start')} to {festival_info.get('peak_bloom_end')}")


def display_optimal_itinerary(itinerary: Dict[str, Any]):
    """Display optimal itinerary recommendation."""
    print("\n" + "=" * 80)
    print("🗓️  OPTIMAL ITINERARY RECOMMENDATION")
    print("=" * 80)
    
    if not itinerary.get("suggested"):
        print(f"❌ {itinerary.get('message', 'Unable to generate recommendation')}")
        return
    
    print(f"\n✈️  Recommended Routing: {itinerary.get('recommended_routing', 'N/A')}")
    
    split = itinerary.get("split", {})
    print(f"\n📅 6-Day Split:")
    print(f"   Washington DC: {split.get('washington_dc', 0)} days")
    print(f"   New York: {split.get('new_york', 0)} days")
    
    first_city = itinerary.get("first_city", "")
    second_city = itinerary.get("second_city", "")
    print(f"\n🗺️  Suggested Order:")
    print(f"   1. Start in {first_city.replace('_', ' ').title()}")
    print(f"   2. Travel to {second_city.replace('_', ' ').title()}")
    
    # Cherry Blossom info
    cherry_info = itinerary.get("cherry_blossom_info")
    if cherry_info and cherry_info.get("overlaps_peak_bloom"):
        print(f"\n🌸 Cherry Blossom Peak Bloom: YES!")
        print(f"   Your trip will catch the peak bloom in DC!")
    
    # Activity suggestions
    suggestions = itinerary.get("suggestions", {})
    if suggestions.get("washington_dc"):
        print(f"\n🏛️  Washington DC Activities:")
        for i, activity in enumerate(suggestions["washington_dc"], 1):
            print(f"   {i}. {activity}")
    
    if suggestions.get("new_york"):
        print(f"\n🗽 New York Activities:")
        for i, activity in enumerate(suggestions["new_york"], 1):
            print(f"   {i}. {activity}")
    
    # Savings info
    savings = itinerary.get("estimated_savings")
    if savings:
        currency = itinerary.get("routing_analysis", {}).get("currency", "USD")
        print(f"\n💰 Estimated Savings: {format_price(savings, currency)} by choosing recommended routing")


def generate_itinerary_for_dates(departure_date: str, return_date: str) -> Dict[str, Any]:
    """Generate itinerary recommendation for specific dates."""
    print(f"\n{'='*80}")
    print(f"📅 GENERATING ITINERARY FOR: {departure_date} → {return_date}")
    print(f"{'='*80}")
    
    db = TravelTrackerDB()
    
    # Check Cherry Blossom
    display_cherry_blossom_info(departure_date, return_date)
    
    # Analyze routing
    routing_analysis = analyze_best_routing(db)
    display_routing_analysis(routing_analysis)
    
    # Generate optimal itinerary
    itinerary = suggest_optimal_itinerary(
        departure_date=departure_date,
        return_date=return_date,
        db=db
    )
    display_optimal_itinerary(itinerary)
    
    return {
        "departure_date": departure_date,
        "return_date": return_date,
        "routing_analysis": routing_analysis,
        "itinerary": itinerary,
        "cherry_blossom": check_cherry_blossom_overlap(departure_date, return_date)
    }


def generate_all_itineraries() -> List[Dict[str, Any]]:
    """Generate itinerary recommendations for all dates in the travel window."""
    dates = get_dates()
    window = dates.get("spring_break_window", {})
    start_date = datetime.strptime(window.get("start", "2026-04-03"), "%Y-%m-%d")
    end_date = datetime.strptime(window.get("end", "2026-04-06"), "%Y-%m-%d")
    trip_duration = dates.get("trip_duration_days", 6)
    
    results = []
    current_date = start_date
    
    print(f"\n{'='*80}")
    print(f"🗓️  GENERATING ITINERARIES FOR ALL DATES")
    print(f"   Window: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"   Trip Duration: {trip_duration} days")
    print(f"{'='*80}")
    
    while current_date <= end_date:
        departure_date = current_date.strftime("%Y-%m-%d")
        return_date = (current_date + timedelta(days=trip_duration)).strftime("%Y-%m-%d")
        
        result = generate_itinerary_for_dates(departure_date, return_date)
        results.append(result)
        
        current_date += timedelta(days=1)
    
    return results


def main():
    """Main function for Phase 5."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Phase 5: Final Itinerary Recommendations")
    parser.add_argument(
        "--dates",
        nargs=2,
        metavar=("DEPART", "RETURN"),
        help="Generate itinerary for specific dates (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate itineraries for all dates in travel window"
    )
    parser.add_argument(
        "--cherry-blossom",
        action="store_true",
        help="Show Cherry Blossom Festival information only"
    )
    
    args = parser.parse_args()
    
    try:
        if args.cherry_blossom:
            # Show Cherry Blossom info for 2026
            cherry_info = get_cherry_blossom_info(2026)
            print("\n" + "=" * 80)
            print("🌸 CHERRY BLOSSOM FESTIVAL 2026")
            print("=" * 80)
            print(f"\n📅 Festival: {cherry_info['festival_start']} to {cherry_info['festival_end']}")
            print(f"🌸 Peak Bloom: {cherry_info['peak_bloom_start']} to {cherry_info['peak_bloom_end']}")
            print(f"📍 Location: {cherry_info['location']}")
            print(f"🌐 Website: {cherry_info['website']}")
        
        elif args.dates:
            departure_date, return_date = args.dates
            generate_itinerary_for_dates(departure_date, return_date)
        
        elif args.all:
            results = generate_all_itineraries()
            print(f"\n{'='*80}")
            print(f"✅ Generated {len(results)} itinerary recommendations")
            print(f"{'='*80}")
        
        else:
            # Default: show general recommendation
            print("\n" + "=" * 80)
            print("🗓️  PHASE 5: FINAL ITINERARY RECOMMENDATIONS")
            print("=" * 80)
            
            db = TravelTrackerDB()
            routing_analysis = analyze_best_routing(db)
            display_routing_analysis(routing_analysis)
            
            itinerary = suggest_optimal_itinerary(db=db)
            display_optimal_itinerary(itinerary)
            
            # Show Cherry Blossom info
            dates = get_dates()
            window = dates.get("spring_break_window", {})
            if window.get("start"):
                display_cherry_blossom_info(
                    window.get("start"),
                    (datetime.strptime(window.get("start"), "%Y-%m-%d") + 
                     timedelta(days=dates.get("trip_duration_days", 6))).strftime("%Y-%m-%d")
                )
    
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
