"""Custom exception classes for Flight Agent."""
from typing import Optional


class FlightAgentError(Exception):
    """Base exception for Flight Agent."""
    pass


class APIError(FlightAgentError):
    """API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.status_code = status_code
        self.original_error = original_error


class ConfigurationError(FlightAgentError):
    """Configuration-related errors."""
    pass


class DatabaseError(FlightAgentError):
    """Database-related errors."""
    pass


class ValidationError(FlightAgentError):
    """Input validation errors."""
    pass


class EmailError(FlightAgentError):
    """Email-related errors."""
    pass
