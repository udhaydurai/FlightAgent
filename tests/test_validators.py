"""Unit tests for input validators."""
import pytest
from datetime import datetime, timedelta
from api.utils.validators import (
    validate_airport_code,
    validate_date,
    validate_passenger_count,
    validate_price
)
from api.utils.errors import ValidationError


class TestValidateAirportCode:
    """Test airport code validation."""
    
    def test_valid_airport_code(self):
        assert validate_airport_code("SAN") == "SAN"
        assert validate_airport_code("jfk") == "JFK"
        assert validate_airport_code("  LAX  ") == "LAX"
    
    def test_invalid_airport_code(self):
        with pytest.raises(ValidationError):
            validate_airport_code("SA")  # Too short
        
        with pytest.raises(ValidationError):
            validate_airport_code("SAND")  # Too long
        
        with pytest.raises(ValidationError):
            validate_airport_code("12A")  # Contains numbers
        
        with pytest.raises(ValidationError):
            validate_airport_code("")  # Empty
        
        with pytest.raises(ValidationError):
            validate_airport_code(None)  # None


class TestValidateDate:
    """Test date validation."""
    
    def test_valid_date(self):
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        assert validate_date(future_date) == future_date
    
    def test_invalid_date_format(self):
        with pytest.raises(ValidationError):
            validate_date("2026/04/03")  # Wrong format
        
        with pytest.raises(ValidationError):
            validate_date("04-03-2026")  # Wrong format
    
    def test_past_date(self):
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        with pytest.raises(ValidationError):
            validate_date(past_date)  # Past date
    
    def test_invalid_date_value(self):
        with pytest.raises(ValidationError):
            validate_date("2026-13-45")  # Invalid month/day


class TestValidatePassengerCount:
    """Test passenger count validation."""
    
    def test_valid_count(self):
        assert validate_passenger_count(1) == 1
        assert validate_passenger_count(5) == 5
        assert validate_passenger_count(9) == 9
    
    def test_invalid_count(self):
        with pytest.raises(ValidationError):
            validate_passenger_count(0)  # Too low
        
        with pytest.raises(ValidationError):
            validate_passenger_count(10)  # Too high
        
        with pytest.raises(ValidationError):
            validate_passenger_count("1")  # Not int


class TestValidatePrice:
    """Test price validation."""
    
    def test_valid_price(self):
        assert validate_price(100.50) == 100.50
        assert validate_price(0) == 0.0
        assert validate_price(None) is None
    
    def test_invalid_price(self):
        with pytest.raises(ValidationError):
            validate_price(-10)  # Negative
        
        with pytest.raises(ValidationError):
            validate_price("100")  # Not number
