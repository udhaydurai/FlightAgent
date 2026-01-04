# Phase 1: Environment & API Foundation - Setup Guide

## ✅ Completed Tasks

1. **Python Environment & Project Structure**
   - ✅ Project structure initialized with `/api` directory
   - ✅ Python modules organized: `services/`, `utils/`
   - ✅ Configuration files in place

2. **Dependencies**
   - ✅ `requirements.txt` includes:
     - `amadeus>=2.0.0` - Amadeus API client
     - `pandas>=2.0.0` - Data manipulation
     - `python-dotenv>=1.0.0` - Environment variable management
     - `requests>=2.31.0` - HTTP requests

3. **Configuration**
   - ✅ `config.json` configured with:
     - Origin: **SAN** (San Diego)
     - Destinations: **DCA, IAD, JFK, LGA, EWR** (all five airports)
     - Open-jaw routing options
     - Travel dates: April 1-10, 2026
     - Filter preferences (nonstop, no red-eyes)

4. **Environment Variables**
   - ✅ `.env.example` template created

## 🚀 Setup Instructions

### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Amadeus API Credentials

1. Sign up for a free account at https://developers.amadeus.com/
2. Create a new app to get your API Key and API Secret
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your credentials:
   ```
   AMADEUS_API_KEY=your_actual_api_key
   AMADEUS_API_SECRET=your_actual_api_secret
   AMADEUS_ENV=test
   ```

### Step 4: Verify Configuration

**Option A: Comprehensive Test (Recommended)**
Run the Phase 1 test suite:
```bash
python api/test_phase1.py
```

This will test:
- ✅ Package imports (amadeus, pandas, dotenv, requests)
- ✅ Configuration loading (config.json)
- ✅ Environment variables (.env file)
- ✅ Amadeus API connection
- ✅ Project structure

**Option B: Individual Tests**
Test the Amadeus API connection:
```bash
python api/test_connection.py
```

Expected output: `✅ Connection successful!`

### Step 5: Verify Config.json

The `config.json` is already configured with:
- **Origin**: SAN
- **Destinations**: DCA, IAD, JFK, LGA, EWR (all five airports)
- **Travel Window**: April 1-10, 2026
- **Constraints**: Nonstop only, no red-eyes

## 📋 Phase 1 Checklist

- [x] Initialize Python environment and project structure
- [x] Install `amadeus-python`, `pandas`, `python-dotenv`, and `requests`
- [x] Create `.env` for Amadeus API Key and Secret (template provided)
- [x] Setup `config.json` with Origin: **SAN** and Destinations: **DCA, IAD, JFK, LGA, EWR**

## 🎯 Next Steps

Once Phase 1 is complete, proceed to **Phase 2: Flexible Multi-City Search Engine** to:
- Fetch flight offers for April 1-10, 2026
- Implement flexible routing (both open-jaw options)
- Apply red-eye and nonstop filters
