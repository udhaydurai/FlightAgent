# View Flight Data from Database

## Quick Usage

### View all recent records
```bash
python api/view_flight_data.py --all
```

### View with detailed flight information
```bash
python api/view_flight_data.py --all --detailed
```

### View records for specific dates
```bash
python api/view_flight_data.py --dates 2026-04-03 2026-04-09
```

### View daily best prices
```bash
# View best price for a specific date
python api/view_flight_data.py --best 2026-04-03

# View all daily best prices (default)
python api/view_flight_data.py --best
```

### Export full flight data as JSON
```bash
# Export record ID 1 to console
python api/view_flight_data.py --export 1

# Export to file
python api/view_flight_data.py --export 1 --output flight_data.json
```

## What's Displayed

### Basic View
- Record ID and dates
- Route information (airports, description)
- Price and currency
- Flight numbers
- Airlines
- Booking URL (if available)

### Detailed View (`--detailed`)
- All basic information
- Outbound flight: departure/arrival times, duration
- Return flight: departure/arrival times, duration
- Full JSON data availability

## Database Fields

The database stores:
- **Full flight data**: Complete Amadeus API responses (JSON)
- **Extracted details**: Flight numbers, airlines, booking URLs
- **Price tracking**: Current price, historical prices
- **Daily best**: Best price per day

## Example Output

```
================================================================================
Record 1 of 5
================================================================================
Record ID: 1
Checked Date: 2026-01-03
Created: 2026-01-03 10:30:45
--------------------------------------------------------------------------------

📅 Dates:
  Departure: 2026-04-03
  Return: 2026-04-09

✈️  Route:
  Inbound: DCA
  Outbound: JFK
  Description: Fly SAN → DC (DCA/IAD), travel DC → NYC by road/train, fly NYC (JFK/LGA/EWR) → SAN

💰 Price:
  Total: USD $219.76

🛫 Flight Numbers:
  AA123, DL456

✈️  Airlines:
  American Airlines, Delta Air Lines
```
