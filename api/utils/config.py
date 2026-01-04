"""Configuration utilities for loading trip parameters."""
import json
import os
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json file."""
    config_path = Path(__file__).parent.parent.parent / "config.json"
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"config.json not found at {config_path}. Please create it with your trip parameters."
        )
    
    with open(config_path, "r") as f:
        return json.load(f)


def get_trip_config() -> Dict[str, Any]:
    """Get trip-specific configuration."""
    config = load_config()
    return config.get("trip", {})


def get_origin() -> str:
    """Get origin airport code."""
    trip_config = get_trip_config()
    origin = trip_config.get("origin")
    if origin == "YOUR_HOME_AIRPORT":
        raise ValueError(
            "Please update config.json with your home airport code (e.g., 'LAX', 'SFO', 'ORD')"
        )
    return origin


def get_destinations() -> Dict[str, list]:
    """Get destination airport codes."""
    trip_config = get_trip_config()
    return trip_config.get("destinations", {})


def get_dates() -> Dict[str, Any]:
    """Get trip date configuration."""
    trip_config = get_trip_config()
    return trip_config.get("dates", {})


def get_preferences() -> Dict[str, Any]:
    """Get user preferences for flight filtering."""
    trip_config = get_trip_config()
    return trip_config.get("preferences", {})


def get_open_jaw_config() -> Dict[str, Any]:
    """Get open-jaw trip configuration."""
    trip_config = get_trip_config()
    return trip_config.get("open_jaw", {})


def is_open_jaw() -> bool:
    """Check if open-jaw itinerary is enabled."""
    open_jaw_config = get_open_jaw_config()
    return open_jaw_config.get("enabled", False)


def get_open_jaw_options() -> list:
    """Get available open-jaw itinerary options."""
    open_jaw_config = get_open_jaw_config()
    return open_jaw_config.get("options", [])
