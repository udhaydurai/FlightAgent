# Testing Guide - Architecture Improvements

## Installation

First, install the new dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `tenacity` - Retry logic
- `pydantic` - Input validation
- `pytest` - Testing framework
- `pytest-mock` - Mocking utilities

## Running Tests

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_validators.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=api --cov-report=html
```

### Manual Testing

#### Test Validators

```bash
python3 -c "
from api.utils.validators import validate_airport_code, validate_date
from datetime import datetime, timedelta

# Test airport code
print('Airport code test:', validate_airport_code('SAN'))

# Test date
future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
print('Date test:', validate_date(future_date))
"
```

#### Test Error Handling

```bash
python3 -c "
from api.utils.errors import APIError, ValidationError

# Test custom exceptions
try:
    raise ValidationError('Test error')
except ValidationError as e:
    print('✅ ValidationError works:', str(e))
"
```

#### Test Logging

```bash
python3 -c "
from api.utils.logger import logger

logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
print('✅ Logging works')
"
```

## Testing Amadeus Client

**Note**: The Amadeus client now has retry logic and better error handling. Test with:

```bash
# This will use retry logic if API fails
python api/test_connection.py
```

## What Was Improved

### ✅ Structured Logging
- Replaced `print()` statements with structured logging
- Logs include timestamps, levels, and context
- Can be configured for file output

### ✅ Retry Logic
- API calls automatically retry up to 3 times
- Exponential backoff (2s, 4s, 8s)
- Only retries on transient errors (ResponseError, ConnectionError)

### ✅ Input Validation
- Airport codes validated (3 uppercase letters)
- Dates validated (format and future dates)
- Passenger counts validated (1-9)
- Prices validated (non-negative)

### ✅ Custom Exceptions
- `APIError` - For API-related errors
- `ValidationError` - For input validation errors
- `DatabaseError` - For database errors
- `ConfigurationError` - For config errors

### ✅ Unit Tests
- Tests for validators
- Tests for AmadeusClient (with mocks)
- Easy to extend with more tests

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest tests/`
3. Test manually with scripts above
4. Verify existing functionality still works
