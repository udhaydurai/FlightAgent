# 🗽 Flight Agent

A travel agent application for finding and tracking flights for East Coast Spring Break trips.

**Automated flight price tracking with email alerts for a 6-day family trip from San Diego to Washington D.C. and New York (April 2026).**

## Trip Structure

**Open-Jaw Multi-City Itinerary:**
- **Origin**: San Diego (SAN)
- **Option 1**: Fly SAN → Washington D.C. (IAD/DCA), travel by road/train to New York (JFK/LGA/EWR), fly NYC → SAN
- **Option 2**: Fly SAN → New York (JFK/LGA/EWR), travel by road/train to Washington D.C. (IAD/DCA), fly WAS → SAN
- **Duration**: 6 days (First week of April 2026)

## Tech Stack

- **Frontend**: Next.js 15 (App Router), Tailwind CSS, TypeScript
- **Backend**: Python, Amadeus API
- **Icons**: Lucide React

## Setup

### Frontend (Next.js)

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

### Backend (Python)

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Amadeus API credentials
```

4. Configure trip parameters:
```bash
# Edit config.json with your:
# - Origin airport code (default: SAN)
# - Destination preferences (WAS: IAD/DCA, NYC: JFK/LGA/EWR)
# - Travel dates (Spring Break window: April 2026)
```

**Note**: The config.json is pre-configured for an open-jaw trip from San Diego to Washington D.C./New York. The system will search both itinerary options (SAN→WAS→NYC→SAN and SAN→NYC→WAS→SAN).

5. Test Amadeus API connection:
```bash
python api/test_connection.py
```

6. **Test Phase 1 Environment (Recommended):**
```bash
python api/test_phase1.py
```
This comprehensive test validates:
- Package imports
- Configuration loading
- Environment variables
- Amadeus API connection
- Project structure

7. Test open-jaw flight search:
```bash
python api/test_open_jaw.py
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

**Note:** The code I created doesn't include real API keys - you must sign up and get your own credentials from Amadeus.

## Project Structure

```
FlightAgent/
├── api/                    # Python backend
│   ├── services/          # API clients (Amadeus, Open-Jaw Search)
│   ├── utils/             # Configuration utilities, flight filters
│   ├── test_connection.py # Connection test script
│   └── test_open_jaw.py   # Open-jaw search test script
├── app/                   # Next.js app directory
├── components/            # React components
├── lib/                   # Utility functions
├── hooks/                 # Custom React hooks
├── config.json            # Trip configuration (origin, destinations, dates)
├── requirements.txt       # Python dependencies
└── package.json           # Node.js dependencies
```

## Features

### ✅ Phase 1: Environment & API Foundation
- Python environment with Amadeus API integration
- Configuration management
- All 5 airports configured (DCA, IAD, JFK, LGA, EWR)

### ✅ Phase 2: Flexible Multi-City Search Engine
- Searches both routing options (SAN→DC/NYC→SAN and SAN→NYC/DC→SAN)
- Red-eye filter (excludes flights departing SAN before 7 AM or arriving after 10 PM)
- Nonstop flights only
- Date window search (April 3-6, 2026)

### ✅ Phase 3: Memory & Comparison
- SQLite database for price tracking
- Daily best price tracking
- Price comparison and history
- Hotel price tracking structure (ready for API integration)

### ✅ Phase 4: Automation & Notification
- Email alerts for price drops > $10
- Daily summary reports
- GitHub Actions for automated daily execution (8:00 AM UTC)

## Automation

The system runs automatically via GitHub Actions:
- **Schedule**: Daily at 8:00 AM UTC
- **Actions**: Searches flights, compares prices, sends email alerts
- **Database**: Tracks all price history

See `PHASE4_SETUP.md` for email configuration and `GITHUB_SETUP.md` for repository setup.

## Development Rules

- Place components in `/components` and logic in `/lib`
- Follow mobile-first responsive design
- Ensure all interactive elements have proper hover and focus states
- Use functional components and arrow functions
- Always use TypeScript with strict type checking
