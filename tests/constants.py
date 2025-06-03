"""Constants used throughout the test suite."""

from enum import StrEnum


class TestTickers(StrEnum):
    """Test ticker symbols."""

    AAPL = "AAPL"
    AAPL_LOWER = "aapl"
    TEST = "TEST"


class TestErrorMessages(StrEnum):
    """Expected error message patterns."""

    ERROR_PREFIX = "Error: "
    MISSING_TICKER = "Missing argument 'TICKER'"


# Test data configuration
SAMPLE_DAYS_LOOKBACK = 30
SAMPLE_BASE_OPEN = 100.0
SAMPLE_BASE_HIGH = 101.0
SAMPLE_BASE_LOW = 99.0
SAMPLE_BASE_CLOSE = 100.5
SAMPLE_VALUE_INCREMENT = 0.5
SAMPLE_BASE_VOLUME = 1000000
SAMPLE_VOLUME_INCREMENT = 10000
SAMPLE_DATE_FREQUENCY = "D"

# Test dates
TEST_DATE_2020 = "2020-01-01"
TEST_PERIODS = 3

# Environment variables
SKIP_INTEGRATION_ENV_VAR = "SKIP_INTEGRATION_TESTS"
