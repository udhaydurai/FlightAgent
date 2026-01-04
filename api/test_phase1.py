"""Comprehensive test script for Phase 1: Environment & API Foundation."""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all required packages can be imported."""
    print("=" * 60)
    print("Testing Package Imports")
    print("=" * 60)
    
    packages = {
        "amadeus": "Amadeus API client",
        "pandas": "Data manipulation",
        "dotenv": "Environment variable management",
        "requests": "HTTP requests"
    }
    
    failed = []
    for package, description in packages.items():
        try:
            if package == "dotenv":
                import dotenv
            else:
                __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError as e:
            print(f"❌ {package:15} - {description}")
            print(f"   Error: {str(e)[:50]}")
            failed.append(package)
        except Exception as e:
            print(f"⚠️  {package:15} - {description}")
            print(f"   Unexpected error: {str(e)[:50]}")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️  Missing packages: {', '.join(failed)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages imported successfully!")
    return True


def test_env_file():
    """Test that .env file exists and has required variables."""
    print("\n" + "=" * 60)
    print("Testing Environment Variables")
    print("=" * 60)
    
    env_path = Path(__file__).parent.parent / ".env"
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Create .env file with your Amadeus API credentials")
        print("   See .env.example for reference")
        return False
    
    print("✅ .env file exists")
    
    # Load and check variables
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping env variable check")
        return False
    
    api_key = os.getenv("AMADEUS_API_KEY")
    api_secret = os.getenv("AMADEUS_API_SECRET")
    env = os.getenv("AMADEUS_ENV", "test")
    
    if not api_key or api_key == "your_api_key_here":
        print("❌ AMADEUS_API_KEY not set or using placeholder")
        return False
    print("✅ AMADEUS_API_KEY is set")
    
    if not api_secret or api_secret == "your_api_secret_here":
        print("❌ AMADEUS_API_SECRET not set or using placeholder")
        return False
    print("✅ AMADEUS_API_SECRET is set")
    
    print(f"✅ AMADEUS_ENV = {env}")
    
    return True


def test_config():
    """Test that config.json is properly configured."""
    print("\n" + "=" * 60)
    print("Testing Configuration")
    print("=" * 60)
    
    try:
        from api.utils.config import (
            load_config,
            get_origin,
            get_destinations,
            get_dates,
            get_preferences
        )
        
        config = load_config()
        print("✅ config.json loaded successfully")
        
        origin = get_origin()
        if origin != "SAN":
            print(f"⚠️  Origin is {origin}, expected SAN")
        else:
            print(f"✅ Origin: {origin}")
        
        destinations = get_destinations()
        all_airports = destinations.get("all_airports", [])
        expected_airports = {"DCA", "IAD", "JFK", "LGA", "EWR"}
        actual_airports = set(all_airports)
        
        if actual_airports == expected_airports:
            print(f"✅ All destinations configured: {', '.join(sorted(all_airports))}")
        else:
            missing = expected_airports - actual_airports
            extra = actual_airports - expected_airports
            if missing:
                print(f"⚠️  Missing airports: {', '.join(missing)}")
            if extra:
                print(f"⚠️  Extra airports: {', '.join(extra)}")
        
        dates = get_dates()
        spring_break = dates.get("spring_break_window", {})
        start = spring_break.get("start", "")
        end = spring_break.get("end", "")
        
        if start == "2026-04-01" and end == "2026-04-10":
            print(f"✅ Travel window: {start} to {end}")
        else:
            print(f"⚠️  Travel window: {start} to {end} (expected 2026-04-01 to 2026-04-10)")
        
        prefs = get_preferences()
        nonstop = prefs.get("nonstop_required", False)
        no_red_eyes = prefs.get("no_red_eyes", False)
        
        if nonstop:
            print("✅ Nonstop flights required")
        else:
            print("⚠️  Nonstop not required")
        
        if no_red_eyes:
            print("✅ Red-eye filter enabled")
        else:
            print("⚠️  Red-eye filter disabled")
        
        return True
    
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_amadeus_connection():
    """Test Amadeus API connection."""
    print("\n" + "=" * 60)
    print("Testing Amadeus API Connection")
    print("=" * 60)
    
    try:
        from api.services.amadeus_client import AmadeusClient
        
        client = AmadeusClient()
        result = client.test_connection()
        
        if result["success"]:
            print("✅ Amadeus API connection successful!")
            print(f"   Message: {result['message']}")
            return True
        else:
            print("❌ Amadeus API connection failed!")
            error = result.get("error", {})
            print(f"   Code: {error.get('code', 'N/A')}")
            print(f"   Description: {error.get('description', 'N/A')}")
            return False
    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   Make sure .env file has AMADEUS_API_KEY and AMADEUS_API_SECRET")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_project_structure():
    """Test that project structure is correct."""
    print("\n" + "=" * 60)
    print("Testing Project Structure")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent
    required_files = [
        "requirements.txt",
        "config.json",
        "api/__init__.py",
        "api/services/__init__.py",
        "api/services/amadeus_client.py",
        "api/utils/__init__.py",
        "api/utils/config.py",
        "api/utils/flight_filter.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing!")
            all_exist = False
    
    return all_exist


def main():
    """Run all Phase 1 tests."""
    print("\n" + "=" * 60)
    print("Phase 1: Environment & API Foundation - Test Suite")
    print("=" * 60)
    
    results = {
        "Project Structure": test_project_structure(),
        "Package Imports": test_imports(),
        "Configuration": test_config(),
        "Environment Variables": test_env_file(),
        "Amadeus Connection": False
    }
    
    # Only test Amadeus if env file is set up
    if results["Environment Variables"]:
        results["Amadeus Connection"] = test_amadeus_connection()
    else:
        print("\n⚠️  Skipping Amadeus connection test (env file not configured)")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Phase 1 is complete and ready for Phase 2.")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
