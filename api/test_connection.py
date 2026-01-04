"""Test script to verify Amadeus API connection."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.amadeus_client import AmadeusClient


def main():
    """Test Amadeus API connection."""
    print("Testing Amadeus API connection...")
    print("-" * 50)
    
    try:
        client = AmadeusClient()
        result = client.test_connection()
        
        if result["success"]:
            print("✅ Connection successful!")
            print(f"Message: {result['message']}")
            if result.get("test_data"):
                print(f"Test data: {result['test_data']}")
        else:
            print("❌ Connection failed!")
            error_info = result.get('error', {})
            print(f"Error: {error_info.get('description', 'Unknown error')}")
            print(f"Code: {error_info.get('code', 'N/A')}")
            print(f"Message: {error_info.get('message', 'N/A')}")
            print()
            print("Note: A 500 error usually means:")
            print("  - The endpoint may not be available in test mode")
            print("  - Or the Amadeus API server is having issues")
            print()
            print("Try running: python api/test_auth_only.py")
            print("This will verify your credentials are valid (OAuth works)")
            return 1
    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure:")
        print("1. .env file exists with AMADEUS_API_KEY and AMADEUS_API_SECRET")
        print("2. Copy .env.example to .env and fill in your credentials")
        return 1
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    print("-" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
