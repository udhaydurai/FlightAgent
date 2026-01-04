"""Phase 2: Flexible Multi-City Search Engine."""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import csv

# Try to import pandas, but make it optional
# Suppress all warnings and errors during import
import warnings
import os
import sys

# Suppress warnings
warnings.filterwarnings('ignore')

# Temporarily redirect stderr to suppress NumPy errors
PANDAS_AVAILABLE = False
_stderr_backup = sys.stderr
try:
    # Redirect stderr to suppress import errors
    with open(os.devnull, 'w') as devnull:
        sys.stderr = devnull
        try:
            import pandas as pd
            PANDAS_AVAILABLE = True
        finally:
            sys.stderr = _stderr_backup
except (ImportError, AttributeError, Exception):
    sys.stderr = _stderr_backup
    PANDAS_AVAILABLE = False

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.open_jaw_search import OpenJawSearch
from api.utils.config import get_dates, get_preferences


def generate_date_range(start_date: str, end_date: str) -> List[str]:
    """Generate list of dates between start and end (inclusive)."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return dates


def calculate_return_date(departure_date: str, trip_duration: int = 6) -> str:
    """Calculate return date based on trip duration."""
    dep = datetime.strptime(departure_date, "%Y-%m-%d")
    ret = dep + timedelta(days=trip_duration)
    return ret.strftime("%Y-%m-%d")


def search_date_window(max_dates: int = None) -> Dict[str, Any]:
    """
    Search for flights across the entire date window (April 1-10, 2026).
    
    Args:
        max_dates: Optional limit on number of dates to search (for testing)
    
    Returns:
        Dictionary with search results for all dates
    """
    dates_config = get_dates()
    spring_break = dates_config.get("spring_break_window", {})
    start_date = spring_break.get("start", "2026-04-01")
    end_date = spring_break.get("end", "2026-04-10")
    trip_duration = dates_config.get("trip_duration_days", 6)
    
    print("=" * 70)
    print("Phase 2: Flexible Multi-City Search Engine")
    print("=" * 70)
    print(f"Search Window: {start_date} to {end_date}")
    print(f"Trip Duration: {trip_duration} days")
    if max_dates:
        print(f"⚠️  Limited to {max_dates} dates for testing")
    print()
    
    # Generate all possible departure dates
    departure_dates = generate_date_range(start_date, end_date)
    
    # Limit dates if specified (for faster testing)
    if max_dates:
        departure_dates = departure_dates[:max_dates]
        print(f"⚠️  Testing with first {max_dates} dates only")
    
    print(f"Searching {len(departure_dates)} departure dates...")
    print("(This may take several minutes - each date searches multiple routes)")
    print("-" * 70)
    
    searcher = OpenJawSearch()
    all_results = []
    start_time = datetime.now()
    
    for i, dep_date in enumerate(departure_dates, 1):
        ret_date = calculate_return_date(dep_date, trip_duration)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        avg_time = elapsed / i if i > 0 else 0
        remaining = avg_time * (len(departure_dates) - i)
        
        print(f"[{i}/{len(departure_dates)}] Searching: Depart {dep_date} → Return {ret_date}")
        if i > 1:
            print(f"  ⏱️  Elapsed: {elapsed:.1f}s | Est. remaining: {remaining:.1f}s")
        
        try:
            result = searcher.search_best_open_jaw(
                departure_date=dep_date,
                return_date=ret_date,
                adults=1
            )
            
            if result.get("success") and result.get("best_option"):
                best = result["best_option"]
                all_results.append({
                    "departure_date": dep_date,
                    "return_date": ret_date,
                    "inbound_airport": best.get("inbound_airport"),
                    "outbound_airport": best.get("outbound_airport"),
                    "description": best.get("description"),
                    "total_price": best.get("total_price"),
                    "currency": best.get("currency"),
                    "outbound_flight": best.get("outbound_flight"),
                    "return_flight": best.get("return_flight")
                })
                print(f"  ✅ Found: ${best.get('total_price', 0):.2f} {best.get('currency', 'USD')}")
            else:
                print(f"  ⚠️  No flights found for this date combination")
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")
        
        print()
    
    # Sort by price
    all_results.sort(key=lambda x: x.get("total_price", float('inf')))
    
    return {
        "success": True,
        "search_window": {
            "start": start_date,
            "end": end_date,
            "trip_duration": trip_duration
        },
        "total_searches": len(departure_dates),
        "results_found": len(all_results),
        "best_options": all_results[:10],  # Top 10 cheapest
        "all_results": all_results
    }


def display_results(results: Dict[str, Any]):
    """Display search results in a formatted way."""
    print("=" * 70)
    print("Search Results Summary")
    print("=" * 70)
    print(f"Total searches: {results['total_searches']}")
    print(f"Results found: {results['results_found']}")
    print()
    
    if results['results_found'] == 0:
        print("⚠️  No flights found matching criteria.")
        print("   This could be because:")
        print("   - Dates are too far in advance (2026)")
        print("   - Filters are too restrictive")
        print("   - API test mode limitations")
        return
    
    print("Top 10 Cheapest Options:")
    print("-" * 70)
    
    for i, option in enumerate(results['best_options'], 1):
        print(f"\n{i}. ${option['total_price']:.2f} {option['currency']}")
        print(f"   Depart: {option['departure_date']} | Return: {option['return_date']}")
        print(f"   Route: {option['description']}")
        print(f"   Inbound: {option['inbound_airport']} | Outbound: {option['outbound_airport']}")


def export_to_csv(results: Dict[str, Any], filename: str = "phase2_results.csv"):
    """Export results to CSV file."""
    if results['results_found'] == 0:
        print("No results to export.")
        return
    
    # Flatten flight details for CSV
    export_data = []
    for row in results['all_results']:
        export_data.append({
            "departure_date": row['departure_date'],
            "return_date": row['return_date'],
            "inbound_airport": row['inbound_airport'],
            "outbound_airport": row['outbound_airport'],
            "total_price": row['total_price'],
            "currency": row['currency'],
            "description": row['description']
        })
    
    # Use pandas if available, otherwise use csv module
    if PANDAS_AVAILABLE:
        try:
            df_export = pd.DataFrame(export_data)
            df_export.to_csv(filename, index=False)
            print(f"\n✅ Results exported to {filename}")
            return
        except Exception as e:
            print(f"⚠️  pandas export failed: {e}, using csv module instead")
    
    # Fallback to csv module
    if export_data:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = export_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(export_data)
        print(f"\n✅ Results exported to {filename}")


def main():
    """Main function for Phase 2 search."""
    import sys
    
    # Allow limiting dates for faster testing
    max_dates = None
    if len(sys.argv) > 1:
        try:
            max_dates = int(sys.argv[1])
            print(f"⚠️  Running in test mode: limiting to {max_dates} dates")
        except ValueError:
            pass
    
    try:
        results = search_date_window(max_dates=max_dates)
        display_results(results)
        
        # Export to CSV
        export_to_csv(results)
        
        total_time = (datetime.now() - datetime.now()).total_seconds()
        print("\n" + "=" * 70)
        print("Phase 2 Search Complete!")
        print("=" * 70)
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Search interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
