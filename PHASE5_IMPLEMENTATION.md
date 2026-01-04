# Phase 5: Final Itinerary - Implementation

## ✅ Completed Features

### 1. Optimal Itinerary Analyzer
- **File**: `api/utils/itinerary_suggestor.py`
- **Features**:
  - Analyzes best flight routing options from database
  - Compares SAN → DC / NYC → SAN vs SAN → NYC / DC → SAN
  - Suggests optimal 6-day split based on cheapest direction
  - Considers Cherry Blossom Festival dates when recommending

### 2. Cherry Blossom Festival Integration
- **File**: `api/utils/itinerary_suggestor.py`
- **Features**:
  - Checks if trip dates overlap with peak bloom (late March - early April)
  - Provides festival dates and peak bloom window
  - Adjusts itinerary recommendations to prioritize DC during peak bloom
  - Includes festival information in recommendations

### 3. Phase 5 Script
- **File**: `api/phase5_itinerary.py`
- **Features**:
  - Generates itinerary recommendations for specific dates
  - Analyzes all dates in travel window
  - Displays routing analysis, Cherry Blossom info, and optimal split
  - Command-line interface for flexible usage

### 4. Email Integration
- **Files**: `api/email_notifier.py`, `api/phase4_automated.py`
- **Features**:
  - Daily email reports now include itinerary suggestions
  - Cherry Blossom peak bloom alerts in emails
  - Recommended routing and 6-day split displayed

## Usage

### Generate Itinerary for All Dates

```bash
python api/phase5_itinerary.py --all
```

This will:
1. Analyze all dates in the travel window (April 3-6, 2026)
2. Check Cherry Blossom overlap for each date
3. Compare routing options
4. Generate optimal itinerary recommendations

### Generate Itinerary for Specific Dates

```bash
python api/phase5_itinerary.py --dates 2026-04-03 2026-04-09
```

### Show Cherry Blossom Information Only

```bash
python api/phase5_itinerary.py --cherry-blossom
```

### Default: General Recommendation

```bash
python api/phase5_itinerary.py
```

Shows overall routing analysis and general itinerary recommendation.

## Output Example

```
================================================================================
📊 FLIGHT ROUTING ANALYSIS
================================================================================

✈️  Option 1: SAN → DC / NYC → SAN
   Routes found: 8
   Average price: USD $450.00
   Best price: USD $420.50
   Dates: 2026-04-03 → 2026-04-09
   Airports: DCA / JFK

✈️  Option 2: SAN → NYC / DC → SAN
   Routes found: 7
   Average price: USD $480.00
   Best price: USD $445.00
   Dates: 2026-04-03 → 2026-04-09
   Airports: JFK / DCA

✅ RECOMMENDED: DC First
   Estimated savings: USD $24.50

================================================================================
🌸 CHERRY BLOSSOM FESTIVAL CHECK
================================================================================

📅 Festival Dates: 2026-03-20 to 2026-04-14
🌸 Peak Bloom: 2026-03-25 to 2026-04-05
📍 Location: Washington, D.C.
🌐 Website: https://nationalcherryblossomfestival.org/

✅ GREAT NEWS! Your trip overlaps with peak bloom!
   Days in DC during peak: 3
   💡 Recommendation: Visit DC first to catch the peak bloom!

================================================================================
🗓️  OPTIMAL ITINERARY RECOMMENDATION
================================================================================

✈️  Recommended Routing: Fly SAN → DC, travel to NYC, fly NYC → SAN

📅 6-Day Split:
   Washington DC: 3 days
   New York: 3 days

🗺️  Suggested Order:
   1. Start in Washington Dc
   2. Travel to New York

🌸 Cherry Blossom Peak Bloom: YES!
   Your trip will catch the peak bloom in DC!

🏛️  Washington DC Activities:
   1. 🌸 See Cherry Blossom Festival peak bloom! (2026-03-25 - 2026-04-05)
   2. Visit National Mall and monuments
   3. Explore Smithsonian museums (free admission)
   ...

💰 Estimated Savings: USD $24.50 by choosing recommended routing
```

## Cherry Blossom Festival

The system checks for overlap with the National Cherry Blossom Festival:
- **Festival Period**: March 20 - April 14, 2026
- **Peak Bloom**: March 25 - April 5, 2026 (estimated)
- **Location**: Washington, D.C.

If your trip overlaps with peak bloom, the system will:
- Recommend visiting DC first
- Adjust the itinerary split to maximize time during peak bloom
- Include festival information in recommendations

## Database Integration

The itinerary analyzer uses data from `travel_tracker.db`:
- Compares prices from `flight_prices` table
- Analyzes routing options (DC first vs NYC first)
- Finds best prices for each routing direction
- Calculates estimated savings

## Email Reports

Daily email reports now include:
- **Itinerary Recommendation**: Suggested routing and 6-day split
- **Cherry Blossom Alerts**: Peak bloom overlap notifications
- **Activity Suggestions**: Things to do in DC and NYC

## Configuration

Itinerary split defaults to 3 days each (configurable in `config.json`):
```json
{
  "preferences": {
    "itinerary_split_days": 3
  }
}
```

## Next Steps

Phase 5 is complete! The system now:
- ✅ Suggests optimal 6-day split based on cheapest flight direction
- ✅ Checks Cherry Blossom peak dates for the report
- ✅ Integrates recommendations into daily email reports
- ✅ Provides comprehensive itinerary analysis
