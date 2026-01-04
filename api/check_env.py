"""Simple script to check .env file configuration."""
import os
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables."""
    base_path = Path(__file__).parent.parent
    env_path = base_path / ".env"
    
    print("=" * 60)
    print("Checking .env File")
    print("=" * 60)
    
    if not env_path.exists():
        print("❌ .env file not found at:", env_path)
        print("\nTo create it, run:")
        print(f"  cd {base_path}")
        print("  cat > .env << 'EOF'")
        print("  AMADEUS_API_KEY=your_api_key_here")
        print("  AMADEUS_API_SECRET=your_secret_here")
        print("  AMADEUS_ENV=test")
        print("  EOF")
        return False
    
    print(f"✅ .env file found at: {env_path}")
    print("\nFile contents:")
    print("-" * 60)
    
    with open(env_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            # Mask the secret for security
            if 'SECRET' in line and '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    print(f"{i}: {parts[0]}=***HIDDEN***")
                else:
                    print(f"{i}: {line.rstrip()}")
            else:
                print(f"{i}: {line.rstrip()}")
    
    print("-" * 60)
    
    # Check for required variables
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        
        api_key = os.getenv("AMADEUS_API_KEY")
        api_secret = os.getenv("AMADEUS_API_SECRET")
        env = os.getenv("AMADEUS_ENV", "test")
        
        print("\nVariable Check:")
        print("-" * 60)
        
        if api_key and api_key != "your_api_key_here":
            print(f"✅ AMADEUS_API_KEY is set (length: {len(api_key)})")
        else:
            print("❌ AMADEUS_API_KEY not set or using placeholder")
        
        if api_secret and api_secret not in ["your_api_secret_here", "your_secret_here"]:
            print(f"✅ AMADEUS_API_SECRET is set (length: {len(api_secret)})")
        else:
            print("❌ AMADEUS_API_SECRET not set or using placeholder")
        
        print(f"✅ AMADEUS_ENV = {env}")
        
        if api_key and api_secret and api_secret not in ["your_api_secret_here", "your_secret_here"]:
            print("\n✅ .env file is properly configured!")
            return True
        else:
            print("\n⚠️  .env file exists but needs API Secret")
            return False
            
    except ImportError:
        print("\n⚠️  python-dotenv not installed, but file exists")
        print("   Install with: pip install python-dotenv")
        return True  # File exists, which is good

if __name__ == "__main__":
    check_env_file()
