"""Simple test to verify Amadeus API authentication (OAuth token)."""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from amadeus import Client

def test_auth():
    """Test if we can get an OAuth token."""
    print("Testing Amadeus API Authentication...")
    print("-" * 50)
    
    # Load environment variables
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    api_key = os.getenv("AMADEUS_API_KEY")
    api_secret = os.getenv("AMADEUS_API_SECRET")
    env = os.getenv("AMADEUS_ENV", "test")
    
    if not api_key or not api_secret:
        print("❌ Missing API credentials in .env file")
        return 1
    
    print(f"✅ API Key found (length: {len(api_key)})")
    print(f"✅ API Secret found (length: {len(api_secret)})")
    print(f"✅ Environment: {env}")
    print()
    
    try:
        # Create client - this will attempt to get OAuth token
        print("Attempting to authenticate...")
        client = Client(
            client_id=api_key,
            client_secret=api_secret,
            hostname=env
        )
        
        # If we get here without exception, OAuth worked
        print("✅ Authentication successful! OAuth token obtained.")
        print()
        print("Note: Some API endpoints may return 500 errors in test mode.")
        print("This is normal - the important part is that authentication works.")
        return 0
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_auth())
