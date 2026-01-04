"""View stored flight details from the database."""
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import TravelTrackerDB
from api.utils.flight_details import extract_flight_summary


def format_flight_details(flight_data_json: str) -> Dict[str, Any]:
    """Parse and format flight data from JSON string."""
    if not flight_data_json:
        return {}
    
    try:
        data = json.loads(flight_data_json)
        return extract_flight_summary(data)
    except (json.JSONDecodeError, TypeError):
        return {}


def display_flight_record(record: Dict[str, Any], detailed: bool = False):
    """Display a single flight record in readable format."""
    print("=" * 80)
    print(f"Record ID: {record.get('id')}")
    print(f"Checked Date: {record.get('checked_date')}")
    print(f"Created: {record.get('created_at')}")
    print("-" * 80)
    
    print(f"\n📅 Dates:")
    print(f"  Departure: {record.get('departure_date')}")
    print(f"  Return: {record.get('return_date')}")
    
    print(f"\n✈️  Route:")
    print(f"  Inbound: {record.get('inbound_airport')}")
    print(f"  Outbound: {record.get('outbound_airport')}")
    print(f"  Description: {record.get('routing_description', 'N/A')}")
    
    print(f"\n💰 Price:")
    print(f"  Total: {record.get('currency', 'USD')} ${record.get('total_price', 0):.2f}")
    
    if record.get('flight_numbers'):
        print(f"\n🛫 Flight Numbers:")
        print(f"  {record.get('flight_numbers')}")
    
    if record.get('airlines'):
        print(f"\n✈️  Airlines:")
        print(f"  {record.get('airlines')}")
    
    if record.get('booking_url'):
        print(f"\n🔗 Booking URL:")
        print(f"  {record.get('booking_url')}")
    
    if detailed:
        # Show outbound flight details
        if record.get('outbound_flight_data'):
            outbound = format_flight_details(record['outbound_flight_data'])
            if outbound:
                print(f"\n📤 Outbound Flight Details:")
                if outbound.get('departure'):
                    print(f"  Departure: {outbound['departure']['airport']} at {outbound['departure']['time']}")
                if outbound.get('arrival'):
                    print(f"  Arrival: {outbound['arrival']['airport']} at {outbound['arrival']['time']}")
                if outbound.get('duration'):
                    print(f"  Duration: {outbound['duration']}")
        
        # Show return flight details
        if record.get('return_flight_data'):
            return_flight = format_flight_details(record['return_flight_data'])
            if return_flight:
                print(f"\n📥 Return Flight Details:")
                if return_flight.get('departure'):
                    print(f"  Departure: {return_flight['departure']['airport']} at {return_flight['departure']['time']}")
                if return_flight.get('arrival'):
                    print(f"  Arrival: {return_flight['arrival']['airport']} at {return_flight['arrival']['time']}")
                if return_flight.get('duration'):
                    print(f"  Duration: {return_flight['duration']}")
        
        # Show full JSON data if requested
        print(f"\n📄 Full Data Available:")
        print(f"  - Outbound flight data: {'Yes' if record.get('outbound_flight_data') else 'No'}")
        print(f"  - Return flight data: {'Yes' if record.get('return_flight_data') else 'No'}")
    
    print()


def view_all_records(limit: int = 10, detailed: bool = False):
    """View all recent flight records."""
    db = TravelTrackerDB()
    records = db.get_all_recent_prices(limit=limit)
    
    if not records:
        print("No flight records found in database.")
        return
    
    print(f"\n📊 Found {len(records)} flight record(s)\n")
    
    for i, record in enumerate(records, 1):
        print(f"\n{'='*80}")
        print(f"Record {i} of {len(records)}")
        print(f"{'='*80}")
        display_flight_record(record, detailed=detailed)


def view_by_dates(departure_date: str, return_date: str, detailed: bool = False):
    """View records for specific dates."""
    db = TravelTrackerDB()
    record = db.get_last_checked_price(departure_date, return_date)
    
    if not record:
        print(f"No records found for {departure_date} → {return_date}")
        return
    
    print(f"\n📅 Records for {departure_date} → {return_date}\n")
    display_flight_record(record, detailed=detailed)
    
    # Also show history
    from api.phase3_tracker import PriceTracker
    tracker = PriceTracker()
    history = tracker.get_price_history(departure_date, return_date)
    
    if len(history) > 1:
        print(f"\n📈 Price History ({len(history)} records):")
        print("-" * 80)
        for h in history[:10]:  # Show last 10
            print(f"  {h['checked_date']}: {h['currency']} ${h['total_price']:.2f} - {h.get('routing_description', 'N/A')}")


def view_daily_best(date: Optional[str] = None):
    """View daily best prices."""
    db = TravelTrackerDB()
    
    if date:
        best = db.get_daily_best_price(date)
        if best:
            print(f"\n🏆 Best Price for {date}:")
            print("-" * 80)
            print(f"  Price: {best['currency']} ${best['best_price']:.2f}")
            print(f"  Route: {best.get('routing_description', 'N/A')}")
            print(f"  Departure: {best.get('departure_date')} → Return: {best.get('return_date')}")
            print(f"  Airports: {best.get('inbound_airport')} / {best.get('outbound_airport')}")
            print(f"  Updated: {best.get('updated_at')}")
        else:
            print(f"No best price record for {date}")
    else:
        # Show all daily best prices
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM daily_best_prices
                ORDER BY date DESC
                LIMIT 20
            """)
            records = [dict(row) for row in cursor.fetchall()]
        
        if not records:
            print("No daily best prices found.")
            return
        
        print(f"\n🏆 Daily Best Prices (Last 20):")
        print("=" * 80)
        for record in records:
            print(f"  {record['date']}: {record['currency']} ${record['best_price']:.2f} - {record.get('routing_description', 'N/A')}")


def export_flight_json(record_id: int, output_file: str = None):
    """Export full flight data as JSON."""
    db = TravelTrackerDB()
    
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flight_prices WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"Record {record_id} not found.")
            return
        
        record = dict(row)
        
        # Parse JSON fields
        if record.get('outbound_flight_data'):
            record['outbound_flight_data'] = json.loads(record['outbound_flight_data'])
        if record.get('return_flight_data'):
            record['return_flight_data'] = json.loads(record['return_flight_data'])
        
        json_output = json.dumps(record, indent=2, default=str)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(json_output)
            print(f"✅ Exported to {output_file}")
        else:
            print(json_output)


def main():
    """Main function with command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="View flight data from database")
    parser.add_argument("--all", action="store_true", help="View all recent records")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of records")
    parser.add_argument("--detailed", action="store_true", help="Show detailed flight information")
    parser.add_argument("--dates", nargs=2, metavar=("DEPART", "RETURN"), help="View records for specific dates")
    parser.add_argument("--best", metavar="DATE", help="View daily best price for date (YYYY-MM-DD)")
    parser.add_argument("--export", type=int, metavar="ID", help="Export record ID as JSON")
    parser.add_argument("--output", metavar="FILE", help="Output file for export")
    
    args = parser.parse_args()
    
    if args.export:
        export_flight_json(args.export, args.output)
    elif args.dates:
        view_by_dates(args.dates[0], args.dates[1], detailed=args.detailed)
    elif args.best:
        view_daily_best(args.best)
    else:
        view_all_records(limit=args.limit, detailed=args.detailed)


if __name__ == "__main__":
    main()
