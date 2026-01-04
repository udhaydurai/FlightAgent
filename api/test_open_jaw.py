"""Test script for open-jaw flight search."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.open_jaw_search import OpenJawSearch
from api.utils.config import get_dates


def main():
    """Test open-jaw flight search."""
    print("Testing Open-Jaw Flight Search")
    print("=" * 60)
    print("Route: SAN → (WAS or NYC) → Ground Travel → (NYC or WAS) → SAN")
    print("=" * 60)
    
    try:
        dates = get_dates()
        spring_break = dates.get("spring_break_window", {})
        departure_date = spring_break.get("start", "2026-04-01")
        return_date = spring_break.get("end", "2026-04-07")
        
        print(f"\nDeparture Date: {departure_date}")
        print(f"Return Date: {return_date}")
        print("\nSearching for open-jaw itineraries...")
        print("-" * 60)
        
        searcher = OpenJawSearch()
        result = searcher.search_best_open_jaw(
            departure_date=departure_date,
            return_date=return_date,
            adults=1
        )
        
        if result["success"]:
            best = result.get("best_option")
            if best:
                print("\n✅ Best Open-Jaw Option Found:")
                print(f"   Description: {best['description']}")
                print(f"   Inbound Airport: {best['inbound_airport']}")
                print(f"   Outbound Airport: {best['outbound_airport']}")
                print(f"   Total Price: {best['currency']} {best['total_price']:.2f}")
                print("\n   Outbound Flight:")
                outbound = best['outbound_flight']
                itinerary = outbound.get("itineraries", [{}])[0]
                segments = itinerary.get("segments", [])
                if segments:
                    first = segments[0]
                    last = segments[-1]
                    print(f"     {first.get('departure', {}).get('iataCode', '')} → "
                          f"{last.get('arrival', {}).get('iataCode', '')}")
                    print(f"     Departure: {first.get('departure', {}).get('at', 'N/A')}")
                    print(f"     Arrival: {last.get('arrival', {}).get('at', 'N/A')}")
                
                print("\n   Return Flight:")
                return_flight = best['return_flight']
                itinerary = return_flight.get("itineraries", [{}])[0]
                segments = itinerary.get("segments", [])
                if segments:
                    first = segments[0]
                    last = segments[-1]
                    print(f"     {first.get('departure', {}).get('iataCode', '')} → "
                          f"{last.get('arrival', {}).get('iataCode', '')}")
                    print(f"     Departure: {first.get('departure', {}).get('at', 'N/A')}")
                    print(f"     Arrival: {last.get('arrival', {}).get('at', 'N/A')}")
            else:
                print("\n⚠️  No flights found matching criteria")
        else:
            print("\n❌ Search failed")
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 1
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
