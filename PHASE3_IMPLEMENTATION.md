# Phase 3: Memory & Comparison - Implementation

## ✅ Completed Features

### 1. SQLite Database (`travel_tracker.db`)
- **File**: `api/database.py`
- **Tables Created**:
  - `flight_prices` - Stores all flight price records
  - `daily_best_prices` - Tracks best price per day
  - `hotel_prices` - Stores hotel price records
- **Indexes**: Created for fast queries on dates and cities

### 2. Price Comparison Logic
- **File**: `api/phase3_tracker.py`
- **Features**:
  - Compares current price vs last checked price
  - Tracks daily best prices
  - Calculates price drops
  - Determines if alerts should be sent (>$10 drop)

### 3. Hotel Price Tracking Structure
- **File**: `api/services/hotel_tracker.py`
- **Features**:
  - Calculates hotel dates for DC and NYC based on trip split
  - Database structure ready for hotel prices
  - Placeholder for hotel API integration

## Usage

### Track Flight Prices

```bash
# Track prices for all dates in config
python api/phase3_tracker.py
```

This will:
1. Search for flights for each date
2. Compare with previous prices in database
3. Update daily best prices
4. Show price drops and alerts

### Database Location

The database is created at: `travel_tracker.db` (project root)

### Database Schema

**flight_prices:**
- Stores all flight searches with prices
- Tracks routing, airports, dates
- Links to daily best prices

**daily_best_prices:**
- One record per day
- Stores the best price found that day
- Links to flight_prices record

**hotel_prices:**
- Stores hotel prices by city and dates
- Ready for hotel API integration

## Price Comparison Logic

1. **First Check**: Saves price, marks as best for the day
2. **Subsequent Checks**:
   - Compares with last checked price
   - Compares with today's best price
   - Updates best if current is lower
   - Calculates price drop

## Alert Logic

Alerts are triggered when:
- Price drops by more than $10 (configurable in `config.json`)
- Compared against last checked price (not daily best)

## Hotel Tracking

Hotel tracking structure is ready:
- Calculates DC/NYC split (default 3 days each)
- Database tables created
- Placeholder for API integration

**To integrate hotel APIs:**
- Add hotel search in `hotel_tracker.py`
- Use Amadeus Hotel API or other services
- Save results using `save_hotel_price()`

## Next Steps (Phase 4)

- Email notifications for price drops
- GitHub Actions for daily automation
- Format email reports with flight details
