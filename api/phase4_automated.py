"""Phase 4: Automated daily tracking and email reports."""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.phase3_tracker import PriceTracker
from api.database import TravelTrackerDB

# Try to import email notifier
try:
    from api.email_notifier import EmailNotifier
    EMAIL_AVAILABLE = True
except (ImportError, ValueError):
    EMAIL_AVAILABLE = False

# Try to import itinerary suggestor
try:
    from api.utils.itinerary_suggestor import suggest_optimal_itinerary
    ITINERARY_AVAILABLE = True
except ImportError:
    ITINERARY_AVAILABLE = False


def run_daily_tracking():
    """Run daily flight tracking and send reports."""
    print("=" * 70)
    print("Phase 4: Automated Daily Tracking")
    print("=" * 70)
    print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track prices
    tracker = PriceTracker()
    results = tracker.track_all_dates()
    
    # Send daily report email
    if EMAIL_AVAILABLE and tracker.email_notifier:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            db = TravelTrackerDB()
            
            # Get today's best price
            today_best = db.get_daily_best_price(today)
            best_price = today_best['best_price'] if today_best else 0
            currency = today_best['currency'] if today_best else "USD"
            
            # Get recent price history
            recent_prices = db.get_all_recent_prices(limit=20)
            
            # Get itinerary suggestion
            itinerary_suggestion = None
            if ITINERARY_AVAILABLE:
                try:
                    itinerary_suggestion = suggest_optimal_itinerary(db=db)
                except Exception as e:
                    print(f"⚠️  Could not generate itinerary suggestion: {e}")
            
            # Send report
            email_sent = tracker.email_notifier.send_daily_report(
                date=today,
                best_price=best_price,
                currency=currency,
                total_searches=results['total_tracked'],
                alerts_count=results['alerts_count'],
                price_history=recent_prices,
                itinerary_suggestion=itinerary_suggestion
            )
            
            if email_sent:
                print(f"📧 Daily report email sent successfully!")
            else:
                print(f"⚠️  Failed to send daily report email")
        except Exception as e:
            print(f"⚠️  Error sending daily report: {e}")
    else:
        print("ℹ️  Email notifications not configured - skipping daily report")
    
    print()
    print("=" * 70)
    print("Daily tracking complete!")
    print("=" * 70)
    
    return results


def main():
    """Main function for automated daily execution."""
    try:
        results = run_daily_tracking()
        
        print(f"\nSummary:")
        print(f"  - Dates tracked: {results['total_tracked']}")
        print(f"  - Alerts triggered: {results['alerts_count']}")
        print(f"  - Email sent: {results.get('email_sent', False)}")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
