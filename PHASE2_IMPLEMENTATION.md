# Phase 2: Flexible Multi-City Search Engine - Implementation

## ✅ Completed Features

### 1. Fetch Flight Offers for Date Window
- **Script**: `api/phase2_search.py`
- **Functionality**: Searches all dates from April 1-10, 2026
- **Output**: Results sorted by price, exported to CSV

### 2. Flexible Routing
- **Implementation**: `api/services/open_jaw_search.py`
- **Options Searched**:
  1. SAN → DC (DCA/IAD) / NYC (JFK/LGA/EWR) → SAN
  2. SAN → NYC (JFK/LGA/EWR) / DC (DCA/IAD) → SAN
- **All airport combinations tested** for best value

### 3. Red-Eye Filter
- **Implementation**: `api/utils/flight_filter.py`
- **Rules Applied**:
  - Excludes flights departing SAN before 7:00 AM
  - Excludes flights arriving East Coast (DCA, IAD, JFK, LGA, EWR) after 10:00 PM
- **Applied automatically** in `search_flights_filtered()`

### 4. Nonstop Filter
- **Implementation**: `api/services/amadeus_client.py`
- **Enforcement**:
  - `nonstop_only=True` parameter added to search methods
  - Filters results to only include flights with 1 segment (nonstop)
  - Applied at API level before additional filtering

## Usage

### Run Phase 2 Search

```bash
# Activate virtual environment
source venv/bin/activate

# Run the search
python api/phase2_search.py
```

### What It Does

1. **Searches all dates** in the window (April 1-10, 2026)
2. **For each date**, calculates return date (6 days later)
3. **Searches both routing options**:
   - SAN→DC / NYC→SAN
   - SAN→NYC / DC→SAN
4. **Applies filters**:
   - Nonstop only
   - No red-eyes
5. **Combines flights** and finds best total price
6. **Exports results** to `phase2_results.csv`

### Output

- Console output with progress and top 10 cheapest options
- CSV file with all results sorted by price
- Summary statistics

## Filter Details

### Nonstop Enforcement
- API calls filter to only 1-segment flights
- Additional validation in `flight_filter.py`
- Config: `nonstop_required: true` in `config.json`

### Red-Eye Filter
- Checks departure time from SAN (must be >= 7:00 AM)
- Checks arrival time to East Coast (must be <= 10:00 PM)
- Config: `red_eye_departure_san_before: "07:00"` and `red_eye_arrival_east_coast_after: "22:00"`

## Files Modified/Created

1. **`api/phase2_search.py`** - Main search script
2. **`api/services/amadeus_client.py`** - Added `nonstop_only` parameter
3. **`api/services/open_jaw_search.py`** - Already implements flexible routing
4. **`api/utils/flight_filter.py`** - Already implements red-eye filter

## Next Steps (Phase 3)

- Initialize SQLite database for price tracking
- Compare current prices against historical best
- Add hotel price tracking
