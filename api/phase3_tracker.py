"""Phase 3: Memory & Comparison - Track and compare prices."""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import TravelTrackerDB
from api.services.open_jaw_search import OpenJawSearch
from api.utils.config import get_dates, get_preferences
from api.utils.price_tracker import should_send_alert

# Try to import email notifier (optional)
try:
    from api.email_notifier import EmailNotifier
    EMAIL_AVAILABLE = True
except (ImportError, ValueError) as e:
    EMAIL_AVAILABLE = False
    print(f"⚠️  Email notifications not available: {e}")


class PriceTracker:
    """Track and compare flight prices."""
    
    def __init__(self):
        """Initialize tracker with database and searcher."""
        self.db = TravelTrackerDB()
        self.searcher = OpenJawSearch()
        self.email_notifier = None
        if EMAIL_AVAILABLE:
            try:
                self.email_notifier = EmailNotifier()
            except Exception as e:
                print(f"⚠️  Email notifier initialization failed: {e}")
                self.email_notifier = None
    
    def track_flight_prices(self, departure_date: str, return_date: str) -> Dict[str, Any]:
        """
        Search for flights and track prices in database.
        
        Args:
            departure_date: Departure date (YYYY-MM-DD)
            return_date: Return date (YYYY-MM-DD)
        
        Returns:
            Dictionary with tracking results
        """
        print(f"Tracking prices for: {departure_date} → {return_date}")
        print("-" * 70)
        
        # Search for best open-jaw option
        result = self.searcher.search_best_open_jaw(
            departure_date=departure_date,
            return_date=return_date,
            adults=1
        )
        
        if not result.get("success") or not result.get("best_option"):
            return {
                "success": False,
                "message": "No flights found",
                "departure_date": departure_date,
                "return_date": return_date
            }
        
        best = result["best_option"]
        current_price = best.get("total_price", 0)
        currency = best.get("currency", "USD")
        
        # Compare and save to database
        comparison = self.db.compare_and_update_best_price(
            departure_date=departure_date,
            return_date=return_date,
            current_price=current_price,
            currency=currency,
            inbound_airport=best.get("inbound_airport"),
            outbound_airport=best.get("outbound_airport"),
            routing_description=best.get("description"),
            outbound_flight_data=best.get("outbound_flight"),
            return_flight_data=best.get("return_flight")
        )
        
        # Check if alert should be sent
        last_price = comparison.get("last_checked_price")
        should_alert = should_send_alert(current_price, last_price)
        
        # Display results
        print(f"Current Price: {currency} ${current_price:.2f}")
        
        if last_price:
            price_drop = comparison.get("price_drop", 0)
            if price_drop > 0:
                print(f"✅ Price dropped by {currency} ${price_drop:.2f}!")
                print(f"   Previous: {currency} ${last_price:.2f}")
            elif price_drop < 0:
                print(f"⚠️  Price increased by {currency} ${abs(price_drop):.2f}")
                print(f"   Previous: {currency} ${last_price:.2f}")
            else:
                print(f"➡️  Price unchanged: {currency} ${current_price:.2f}")
        else:
            print("📝 First time tracking this date combination")
        
        if comparison.get("is_new_best_today"):
            print(f"🏆 New best price for today!")
        
        if should_alert:
            print(f"🔔 ALERT: Price drop > $10 threshold!")
            
            # Send email notification
            if self.email_notifier:
                try:
                    # Get flight details from database record
                    record = self.db.get_last_checked_price(departure_date, return_date)
                    flight_numbers = record.get('flight_numbers') if record else None
                    airlines = record.get('airlines') if record else None
                    booking_url = record.get('booking_url') if record else None
                    
                    email_sent = self.email_notifier.send_price_drop_alert(
                        departure_date=departure_date,
                        return_date=return_date,
                        current_price=current_price,
                        previous_price=last_price,
                        price_drop=comparison.get("price_drop", 0),
                        currency=currency,
                        inbound_airport=best.get("inbound_airport"),
                        outbound_airport=best.get("outbound_airport"),
                        routing_description=best.get("description"),
                        flight_numbers=flight_numbers,
                        airlines=airlines,
                        booking_url=booking_url
                    )
                    
                    if email_sent:
                        print(f"📧 Email alert sent successfully!")
                    else:
                        print(f"⚠️  Failed to send email alert")
                except Exception as e:
                    print(f"⚠️  Error sending email: {e}")
            else:
                print(f"ℹ️  Email notifications not configured")
        
        print()
        
        return {
            "success": True,
            "departure_date": departure_date,
            "return_date": return_date,
            "comparison": comparison,
            "should_alert": should_alert,
            "email_sent": should_alert and self.email_notifier is not None
        }
    
    def track_all_dates(self) -> Dict[str, Any]:
        """Track prices for all dates in the search window."""
        dates_config = get_dates()
        spring_break = dates_config.get("spring_break_window", {})
        start_date = spring_break.get("start", "2026-04-03")
        end_date = spring_break.get("end", "2026-04-06")
        trip_duration = dates_config.get("trip_duration_days", 6)
        
        from datetime import timedelta
        
        print("=" * 70)
        print("Phase 3: Memory & Comparison")
        print("=" * 70)
        print(f"Tracking prices for: {start_date} to {end_date}")
        print(f"Trip Duration: {trip_duration} days")
        print()
        
        # Generate dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        results = []
        alerts = []
        
        current = start
        while current <= end:
            dep_date = current.strftime("%Y-%m-%d")
            ret_date = (current + timedelta(days=trip_duration)).strftime("%Y-%m-%d")
            
            result = self.track_flight_prices(dep_date, ret_date)
            results.append(result)
            
            if result.get("should_alert"):
                alerts.append(result)
            
            current += timedelta(days=1)
        
        # Summary
        print("=" * 70)
        print("Tracking Summary")
        print("=" * 70)
        print(f"Total dates tracked: {len(results)}")
        print(f"Alerts triggered: {len(alerts)}")
        
        if alerts:
            print("\n🔔 Price Drop Alerts:")
            for alert in alerts:
                comp = alert.get("comparison", {})
                print(f"  - {alert['departure_date']}: "
                      f"${comp.get('price_drop', 0):.2f} drop")
        
        return {
            "success": True,
            "results": results,
            "alerts": alerts,
            "total_tracked": len(results),
            "alerts_count": len(alerts)
        }
    
    def get_price_history(self, departure_date: str, return_date: str) -> list:
        """Get price history for a specific date combination."""
        with self.db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT checked_date, total_price, currency, routing_description
                FROM flight_prices
                WHERE departure_date = ? AND return_date = ?
                ORDER BY checked_date DESC, created_at DESC
            """, (departure_date, return_date))
            
            return [dict(row) for row in cursor.fetchall()]


def main():
    """Main function for Phase 3."""
    try:
        tracker = PriceTracker()
        results = tracker.track_all_dates()
        
        print("\n" + "=" * 70)
        print("Phase 3 Complete!")
        print("=" * 70)
        print(f"Database: travel_tracker.db")
        print(f"Records saved: {results['total_tracked']}")
        print(f"Alerts: {results['alerts_count']}")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Tracking interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
