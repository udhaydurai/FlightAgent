"""Unit tests for AmadeusClient."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from amadeus import ResponseError
from api.utils.errors import APIError, ValidationError
from api.services.amadeus_client import AmadeusClient


class TestAmadeusClient:
    """Test AmadeusClient."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock Amadeus client."""
        with patch('api.services.amadeus_client.Client') as mock:
            yield mock
    
    @pytest.fixture
    def amadeus_client(self, mock_client):
        """Create AmadeusClient instance with mocked dependencies."""
        with patch.dict('os.environ', {
            'AMADEUS_API_KEY': 'test_key',
            'AMADEUS_API_SECRET': 'test_secret',
            'AMADEUS_ENV': 'test'
        }):
            return AmadeusClient()
    
    def test_init_missing_credentials(self):
        """Test initialization with missing credentials."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="AMADEUS_API_KEY"):
                AmadeusClient()
    
    def test_search_flights_validation(self, amadeus_client):
        """Test input validation in search_flights."""
        # Invalid airport code
        with pytest.raises(ValidationError):
            amadeus_client.search_flights(
                origin="SA",  # Too short
                destination="JFK",
                departure_date="2026-04-03"
            )
        
        # Invalid date
        with pytest.raises(ValidationError):
            amadeus_client.search_flights(
                origin="SAN",
                destination="JFK",
                departure_date="2025-01-01"  # Past date
            )
        
        # Invalid passenger count
        with pytest.raises(ValidationError):
            amadeus_client.search_flights(
                origin="SAN",
                destination="JFK",
                departure_date="2026-04-03",
                adults=0  # Invalid
            )
    
    @patch('api.services.amadeus_client.logger')
    def test_search_flights_success(self, mock_logger, amadeus_client):
        """Test successful flight search."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.data = [
            {
                "itineraries": [{
                    "segments": [{"departure": {"iataCode": "SAN"}}]
                }],
                "price": {"total": "500.00", "currency": "USD"}
            }
        ]
        mock_response.dictionaries = {}
        
        amadeus_client.client.shopping.flight_offers_search.get = Mock(return_value=mock_response)
        
        result = amadeus_client.search_flights(
            origin="SAN",
            destination="JFK",
            departure_date="2026-04-03"
        )
        
        assert result["success"] is True
        assert len(result["data"]) == 1
        mock_logger.info.assert_called()
    
    def test_search_flights_api_error(self, amadeus_client):
        """Test API error handling."""
        # Create a proper mock response for ResponseError
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.parsed = True
        mock_response.result = {}
        
        # Create ResponseError with proper mock
        mock_error = ResponseError(mock_response)
        mock_error.description = "Invalid request"
        mock_error.response = mock_response
        
        amadeus_client.client.shopping.flight_offers_search.get = Mock(side_effect=mock_error)
        
        with pytest.raises(APIError) as exc_info:
            amadeus_client.search_flights(
                origin="SAN",
                destination="JFK",
                departure_date="2026-04-03"
            )
        
        assert "Amadeus API error" in str(exc_info.value)
        assert exc_info.value.status_code == 400
