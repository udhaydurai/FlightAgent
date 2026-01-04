"""SQLite database for tracking flight and hotel prices."""
import sqlite3
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from contextlib import contextmanager


class TravelTrackerDB:
    """Database manager for tracking travel prices."""
    
    def __init__(self, db_path: str = "travel_tracker.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self._init_database()
    
    def _get_db_path(self) -> Path:
        """Get full path to database file."""
        # Store in project root
        base_path = Path(__file__).parent.parent
        return base_path / self.db_path
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        db_file = self._get_db_path()
        conn = sqlite3.connect(str(db_file))
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Flight prices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flight_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    departure_date TEXT NOT NULL,
                    return_date TEXT NOT NULL,
                    inbound_airport TEXT NOT NULL,
                    outbound_airport TEXT NOT NULL,
                    routing_description TEXT,
                    total_price REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    outbound_flight_data TEXT,
                    return_flight_data TEXT,
                    booking_url TEXT,
                    flight_numbers TEXT,
                    airlines TEXT,
                    checked_date TEXT NOT NULL,
                    is_best_price INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Daily best prices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_best_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL UNIQUE,
                    best_price REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    departure_date TEXT,
                    return_date TEXT,
                    inbound_airport TEXT,
                    outbound_airport TEXT,
                    routing_description TEXT,
                    flight_record_id INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (flight_record_id) REFERENCES flight_prices(id)
                )
            """)
            
            # Hotel prices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hotel_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    check_in_date TEXT NOT NULL,
                    check_out_date TEXT NOT NULL,
                    hotel_name TEXT,
                    price_per_night REAL NOT NULL,
                    total_price REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    hotel_data TEXT,
                    checked_date TEXT NOT NULL,
                    is_best_price INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(city, check_in_date, check_out_date, hotel_name)
                )
            """)
            
            # Create indexes for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_flight_dates 
                ON flight_prices(departure_date, return_date)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_flight_checked_date 
                ON flight_prices(checked_date)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hotel_city_dates 
                ON hotel_prices(city, check_in_date, check_out_date)
            """)
            
            conn.commit()
    
    def save_flight_price(
        self,
        departure_date: str,
        return_date: str,
        inbound_airport: str,
        outbound_airport: str,
        total_price: float,
        currency: str,
        routing_description: str = "",
        outbound_flight_data: Optional[Dict] = None,
        return_flight_data: Optional[Dict] = None,
        booking_url: Optional[str] = None,
        flight_numbers: Optional[str] = None,
        airlines: Optional[str] = None
    ) -> int:
        """
        Save a flight price record.
        
        Returns:
            ID of the inserted record
        """
        import json
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            checked_date = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute("""
                INSERT INTO flight_prices 
                (departure_date, return_date, inbound_airport, outbound_airport,
                 routing_description, total_price, currency, outbound_flight_data,
                 return_flight_data, booking_url, flight_numbers, airlines, checked_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                departure_date,
                return_date,
                inbound_airport,
                outbound_airport,
                routing_description,
                total_price,
                currency,
                json.dumps(outbound_flight_data) if outbound_flight_data else None,
                json.dumps(return_flight_data) if return_flight_data else None,
                booking_url,
                flight_numbers,
                airlines,
                checked_date
            ))
            
            return cursor.lastrowid
    
    def get_last_checked_price(
        self,
        departure_date: str,
        return_date: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get the last checked price for a specific date combination.
        
        Returns:
            Dictionary with price info or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM flight_prices
                WHERE departure_date = ? AND return_date = ?
                ORDER BY checked_date DESC, created_at DESC
                LIMIT 1
            """, (departure_date, return_date))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def get_daily_best_price(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Get the daily best price for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
        
        Returns:
            Dictionary with best price info or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM daily_best_prices
                WHERE date = ?
            """, (date,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def update_daily_best_price(
        self,
        date: str,
        best_price: float,
        currency: str,
        departure_date: str,
        return_date: str,
        inbound_airport: str,
        outbound_airport: str,
        routing_description: str,
        flight_record_id: int
    ):
        """Update or insert daily best price."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO daily_best_prices
                (date, best_price, currency, departure_date, return_date,
                 inbound_airport, outbound_airport, routing_description,
                 flight_record_id, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                date,
                best_price,
                currency,
                departure_date,
                return_date,
                inbound_airport,
                outbound_airport,
                routing_description,
                flight_record_id
            ))
    
    def compare_and_update_best_price(
        self,
        departure_date: str,
        return_date: str,
        current_price: float,
        currency: str,
        inbound_airport: str,
        outbound_airport: str,
        routing_description: str = "",
        outbound_flight_data: Optional[Dict] = None,
        return_flight_data: Optional[Dict] = None,
        booking_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare current price with last checked price and update if it's better.
        
        Returns:
            Dictionary with comparison results
        """
        checked_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get last checked price for this date combination
        last_price_record = self.get_last_checked_price(departure_date, return_date)
        
        # Get today's best price
        today_best = self.get_daily_best_price(checked_date)
        
        # Extract flight details
        from api.utils.flight_details import (
            extract_flight_numbers,
            extract_airlines
        )
        
        # Combine flight numbers from both flights
        outbound_numbers = extract_flight_numbers(outbound_flight_data) if outbound_flight_data else ""
        return_numbers = extract_flight_numbers(return_flight_data) if return_flight_data else ""
        all_numbers = ", ".join(filter(None, [outbound_numbers, return_numbers]))
        
        # Combine airlines
        outbound_airlines = extract_airlines(outbound_flight_data) if outbound_flight_data else ""
        return_airlines = extract_airlines(return_flight_data) if return_flight_data else ""
        all_airlines = ", ".join(set(filter(None, [outbound_airlines, return_airlines])))
        
        # Save current price
        record_id = self.save_flight_price(
            departure_date=departure_date,
            return_date=return_date,
            inbound_airport=inbound_airport,
            outbound_airport=outbound_airport,
            total_price=current_price,
            currency=currency,
            routing_description=routing_description,
            outbound_flight_data=outbound_flight_data,
            return_flight_data=return_flight_data,
            booking_url=booking_url,
            flight_numbers=all_numbers,
            airlines=all_airlines
        )
        
        # Compare with today's best
        is_new_best = False
        if today_best is None or current_price < today_best['best_price']:
            is_new_best = True
            self.update_daily_best_price(
                date=checked_date,
                best_price=current_price,
                currency=currency,
                departure_date=departure_date,
                return_date=return_date,
                inbound_airport=inbound_airport,
                outbound_airport=outbound_airport,
                routing_description=routing_description,
                flight_record_id=record_id
            )
        
        # Calculate price drop compared to last check
        price_drop = None
        if last_price_record:
            price_drop = last_price_record['total_price'] - current_price
        
        return {
            "current_price": current_price,
            "currency": currency,
            "last_checked_price": last_price_record['total_price'] if last_price_record else None,
            "price_drop": price_drop,
            "is_new_best_today": is_new_best,
            "today_best_price": today_best['best_price'] if today_best else current_price,
            "record_id": record_id
        }
    
    def save_hotel_price(
        self,
        city: str,
        check_in_date: str,
        check_out_date: str,
        price_per_night: float,
        total_price: float,
        currency: str = "USD",
        hotel_name: str = "",
        hotel_data: Optional[Dict] = None
    ) -> int:
        """Save a hotel price record."""
        import json
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            checked_date = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute("""
                INSERT OR REPLACE INTO hotel_prices
                (city, check_in_date, check_out_date, hotel_name,
                 price_per_night, total_price, currency, hotel_data, checked_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                city,
                check_in_date,
                check_out_date,
                hotel_name,
                price_per_night,
                total_price,
                currency,
                json.dumps(hotel_data) if hotel_data else None,
                checked_date
            ))
            
            return cursor.lastrowid
    
    def get_hotel_prices(
        self,
        city: str,
        check_in_date: str,
        check_out_date: str
    ) -> List[Dict[str, Any]]:
        """Get hotel prices for a specific city and date range."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM hotel_prices
                WHERE city = ? AND check_in_date = ? AND check_out_date = ?
                ORDER BY total_price ASC
            """, (city, check_in_date, check_out_date))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_recent_prices(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent flight price records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM flight_prices
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
