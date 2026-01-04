# 🗽 Flight Agent

A travel agent application for finding and tracking flights for East Coast Spring Break trips.

**Automated flight price tracking with email alerts for a 6-day family trip from San Diego to Washington D.C. and New York (April 2026).**

## Trip Structure

**Open-Jaw Multi-City Itinerary:**
- **Origin**: San Diego (SAN)
- **Option 1**: Fly SAN → Washington D.C. (IAD/DCA), travel by road/train to New York (JFK/LGA/EWR), fly NYC → SAN
- **Option 2**: Fly SAN → New York (JFK/LGA/EWR), travel by road/train to Washington D.C. (IAD/DCA), fly WAS → SAN
- **Duration**: 6 days (First week of April 2026)
- **Constraints**: Nonstop flights only, no red-eyes (7 AM - 9 PM departures), price drop alerts > $10

## Tech Stack

- **Frontend**: Next.js 15 (App Router), Tailwind CSS, TypeScript
- **Backend**: Python 3.9+, Amadeus API, SQLite
- **Icons**: Lucide React
- **Automation**: GitHub Actions

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/udhaydurai/FlightAgent.git
cd FlightAgent
```

### 2. Backend Setup (Python)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Amadeus API credentials (see below)
```

### 3. Configure Trip Parameters

Edit `config.json` with your preferences:
- Origin airport (default: SAN)
- Destination airports (DCA, IAD, JFK, LGA, EWR)
- Travel dates (Spring Break window: April 2026)
- Filter preferences (nonstop, no red-eyes)

### 4. Test Setup

```bash
# Comprehensive Phase 1 test (recommended)
python api/test_phase1.py

# Or test individual components
python api/test_connection.py      # Test Amadeus API connection
python api/test_auth_only.py        # Test API authentication only
python api/test_open_jaw.py         # Test open-jaw flight search
```

## Amadeus API Setup

**You need to get your own API credentials!** See `AMADEUS_API_SETUP.md` for detailed instructions.

Quick steps:
1. Sign up for a free account at https://developers.amadeus.com/
2. Create a new app in "My Self-Service Workspace"
3. Copy your API Key and API Secret
4. Add credentials to `.env` file:
   ```
   AMADEUS_API_KEY=your_actual_api_key_here
   AMADEUS_API_SECRET=your_actual_api_secret_here
   AMADEUS_ENV=test  # Use 'test' for development, 'production' for live
   ```

**Note:** The code doesn't include real API keys - you must sign up and get your own credentials from Amadeus.

## Project Phases

### ✅ Phase 1: Environment & API Foundation

**Status**: Complete

**Features:**
- Python environment with virtual environment support
- Amadeus API integration and authentication
- Configuration management (`config.json`)
- All 5 airports configured (DCA, IAD, JFK, LGA, EWR)
- Environment variable management (`.env`)

**Test Scripts:**
```bash
python api/test_phase1.py        # Comprehensive Phase 1 test suite
python api/test_connection.py    # Test Amadeus API connection
python api/test_auth_only.py     # Test API authentication only
```

**Documentation**: See `PHASE1_SETUP.md`

---

### ✅ Phase 2: Flexible Multi-City Search Engine

**Status**: Complete

**Features:**
- Searches both routing options (SAN→DC/NYC→SAN and SAN→NYC/DC→SAN)
- Red-eye filter (excludes flights departing SAN before 7 AM or arriving after 10 PM)
- Nonstop flights only (configurable)
- Date window search (April 3-6, 2026)
- All airport combinations tested
- Results exported to CSV

**Usage:**
```bash
python api/phase2_search.py
```

**Test Scripts:**
```bash
python api/test_open_jaw.py     # Test open-jaw flight search logic
```

**Documentation**: See `PHASE2_IMPLEMENTATION.md`

---

### ✅ Phase 3: Memory & Comparison

**Status**: Complete

**Features:**
- SQLite database (`travel_tracker.db`) for price tracking
- Daily best price tracking
- Price comparison and history
- Flight details storage (full JSON from Amadeus API)
- Hotel price tracking structure (ready for API integration)

**Usage:**
```bash
# Track prices for all dates in config
python api/phase3_tracker.py

# View flight data from database
python api/view_flight_data.py --all
python api/view_flight_data.py --dates 2026-04-03 2026-04-09
python api/view_flight_data.py --best 2026-04-03
```

**Database Schema:**
- `flight_prices` - All flight price records with full flight data
- `daily_best_prices` - Best price per day
- `hotel_prices` - Hotel price tracking (structure ready)

**Documentation**: See `PHASE3_IMPLEMENTATION.md` and `VIEW_FLIGHT_DATA.md`

---

### ✅ Phase 4: Automation & Notification

**Status**: Complete

**Features:**
- Email alerts for price drops > $10 (configurable)
- Daily summary reports with price history
- GitHub Actions for automated daily execution (8:00 AM UTC)
- Gmail App Password support
- HTML email templates

**Usage:**
```bash
# Run automated tracking (local)
python api/phase4_automated.py
```

**Email Configuration:**
1. Create Gmail App Password (see `GMAIL_APP_PASSWORD.md`)
2. Add to `.env` or GitHub Secrets:
   ```
   SENDER_EMAIL=your.email@gmail.com
   SENDER_PASSWORD=your_16_char_app_password
   RECIPIENT_EMAIL=recipient@email.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

**GitHub Actions:**
- Workflow: `.github/workflows/daily_tracking.yml`
- Schedule: Daily at 8:00 AM UTC
- Actions: Searches flights, compares prices, sends email alerts
- Database: Uploaded as artifact after each run

**Documentation**: See `PHASE4_SETUP.md` and `GITHUB_SETUP.md`

---

### ✅ Phase 5: Final Itinerary

**Status**: Complete

**Features:**
- Optimal 6-day split suggestion based on cheapest flight direction
- Cherry Blossom Festival peak bloom date checking
- Routing analysis (DC-first vs NYC-first comparison)
- Activity suggestions for DC and NYC
- Integration with daily email reports

**Usage:**
```bash
# Generate itinerary for all dates
python api/phase5_itinerary.py --all

# Generate for specific dates
python api/phase5_itinerary.py --dates 2026-04-03 2026-04-09

# Show Cherry Blossom info only
python api/phase5_itinerary.py --cherry-blossom

# General recommendation (default)
python api/phase5_itinerary.py
```

**Cherry Blossom Festival:**
- Festival Period: March 20 - April 14, 2026
- Peak Bloom: March 25 - April 5, 2026 (estimated)
- Location: Washington, D.C.
- System adjusts itinerary to prioritize DC during peak bloom

**Documentation**: See `PHASE5_IMPLEMENTATION.md`

---

## Testing

### Test Scripts Overview

| Script | Purpose | Phase |
|--------|---------|-------|
| `api/test_phase1.py` | Comprehensive Phase 1 test suite | Phase 1 |
| `api/test_connection.py` | Test Amadeus API connection | Phase 1 |
| `api/test_auth_only.py` | Test API authentication only | Phase 1 |
| `api/test_open_jaw.py` | Test open-jaw flight search | Phase 2 |

### Running Tests

```bash
# Activate virtual environment first
source venv/bin/activate

# Phase 1 comprehensive test (recommended first step)
python api/test_phase1.py

# Individual component tests
python api/test_connection.py
python api/test_auth_only.py
python api/test_open_jaw.py
```

### Test Coverage

**Phase 1 Tests** (`test_phase1.py`):
- ✅ Package imports (amadeus, pandas, dotenv, requests)
- ✅ Configuration loading (`config.json`)
- ✅ Environment variables (`.env` file)
- ✅ Amadeus API connection
- ✅ Project structure validation

**Connection Tests**:
- `test_connection.py` - Full API connection test
- `test_auth_only.py` - Authentication-only test (isolates credential issues)

**Phase 2 Tests**:
- `test_open_jaw.py` - Open-jaw multi-city search logic

---

## Project Structure

```
FlightAgent/
├── api/                          # Python backend
│   ├── services/                # API clients
│   │   ├── amadeus_client.py   # Amadeus API client
│   │   ├── open_jaw_search.py  # Open-jaw search logic
│   │   └── hotel_tracker.py    # Hotel tracking (structure)
│   ├── utils/                   # Utilities
│   │   ├── config.py           # Configuration loader
│   │   ├── flight_filter.py    # Flight filtering logic
│   │   ├── flight_details.py   # Flight detail extraction
│   │   ├── itinerary_suggestor.py  # Phase 5: Itinerary suggestions
│   │   └── price_tracker.py    # Price comparison logic
│   ├── database.py             # SQLite database manager
│   ├── email_notifier.py       # Email notification system
│   ├── phase2_search.py        # Phase 2: Flight search
│   ├── phase3_tracker.py       # Phase 3: Price tracking
│   ├── phase4_automated.py     # Phase 4: Automated tracking
│   ├── phase5_itinerary.py     # Phase 5: Itinerary recommendations
│   ├── view_flight_data.py     # Database viewer
│   ├── test_phase1.py          # Phase 1 test suite
│   ├── test_connection.py      # Connection test
│   ├── test_auth_only.py       # Auth-only test
│   └── test_open_jaw.py        # Open-jaw test
├── app/                         # Next.js app directory
├── components/                  # React components
├── lib/                         # Utility functions
├── hooks/                       # Custom React hooks
├── .github/
│   └── workflows/
│       └── daily_tracking.yml   # GitHub Actions workflow
├── config.json                  # Trip configuration
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── travel_tracker.db            # SQLite database (generated)
```

---

## Automation

The system runs automatically via GitHub Actions:

- **Schedule**: Daily at 8:00 AM UTC
- **Workflow**: `.github/workflows/daily_tracking.yml`
- **Actions**:
  1. Checkout repository
  2. Set up Python 3.9
  3. Install dependencies
  4. Run `api/phase4_automated.py`
  5. Upload database as artifact
- **Email**: Sends daily reports and price drop alerts
- **Database**: Tracks all price history

**Setup**: See `GITHUB_SETUP.md` for repository and secrets configuration.

---

## Configuration

### Environment Variables (`.env`)

```bash
# Amadeus API
AMADEUS_API_KEY=your_api_key
AMADEUS_API_SECRET=your_api_secret
AMADEUS_ENV=test  # or 'production'

# Email (for Phase 4)
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_app_password  # Gmail App Password
RECIPIENT_EMAIL=recipient@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Trip Configuration (`config.json`)

- **Origin**: San Diego (SAN)
- **Destinations**: DCA, IAD, JFK, LGA, EWR
- **Travel Window**: April 3-6, 2026 (departure dates)
- **Trip Duration**: 6 days
- **Preferences**:
  - No red-eyes: 7 AM - 9 PM departures
  - Nonstop flights only
  - Price drop alert threshold: $10

---

## Documentation

- `PHASE1_SETUP.md` - Phase 1 setup and testing
- `PHASE2_IMPLEMENTATION.md` - Phase 2 flight search details
- `PHASE3_IMPLEMENTATION.md` - Phase 3 database and tracking
- `PHASE4_SETUP.md` - Phase 4 automation and email setup
- `PHASE5_IMPLEMENTATION.md` - Phase 5 itinerary recommendations
- `AMADEUS_API_SETUP.md` - Amadeus API credentials setup
- `GITHUB_SETUP.md` - GitHub repository and Actions setup
- `GMAIL_APP_PASSWORD.md` - Gmail App Password setup
- `VIEW_FLIGHT_DATA.md` - Database viewing guide

---

## Features Summary

✅ **Multi-City Search**: Open-jaw routing with both direction options  
✅ **Smart Filtering**: Red-eye exclusion, nonstop preference  
✅ **Price Tracking**: SQLite database with daily best prices  
✅ **Price Alerts**: Email notifications for price drops > $10  
✅ **Automation**: GitHub Actions daily execution  
✅ **Itinerary Planning**: Optimal split suggestions with Cherry Blossom integration  
✅ **Currency Support**: USD prices (configurable)  
✅ **Email Reports**: HTML daily reports with itinerary suggestions  

---

## Development Rules

- Place components in `/components` and logic in `/lib`
- Follow mobile-first responsive design
- Ensure all interactive elements have proper hover and focus states
- Use functional components and arrow functions
- Always use TypeScript with strict type checking

---

## Troubleshooting

### Common Issues

**Amadeus API Errors:**
- Verify API credentials in `.env`
- Check `AMADEUS_ENV` is set to `test` for development
- Run `python api/test_auth_only.py` to isolate authentication issues

**Email Not Sending:**
- Use Gmail App Password, not regular password
- See `GMAIL_APP_PASSWORD.md` for setup instructions
- Verify all email variables in `.env` or GitHub Secrets

**Database Issues:**
- Database is created automatically on first run
- Download from GitHub Actions artifacts if needed
- Use `python api/view_flight_data.py` to inspect data

**NumPy Compatibility:**
- If you see NumPy errors, run `fix_numpy.sh` or `fix_numpy_quick.sh`
- Or manually: `pip install "numpy<2.0.0"`

---

## License

This project is for personal use. Amadeus API requires your own credentials.

---

## Contributing

This is a personal project, but suggestions and improvements are welcome!
