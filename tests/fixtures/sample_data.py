"""Sample data fixtures for testing."""

from datetime import datetime, timedelta

import pandas as pd

from heisenbux.constants import (
    CLOSE_COLUMN,
    DATE_COLUMN,
    HIGH_COLUMN,
    LOW_COLUMN,
    OPEN_COLUMN,
    VOLUME_COLUMN,
)
from tests.constants import (
    SAMPLE_BASE_CLOSE,
    SAMPLE_BASE_HIGH,
    SAMPLE_BASE_LOW,
    SAMPLE_BASE_OPEN,
    SAMPLE_BASE_VOLUME,
    SAMPLE_DATE_FREQUENCY,
    SAMPLE_DAYS_LOOKBACK,
    SAMPLE_VALUE_INCREMENT,
    SAMPLE_VOLUME_INCREMENT,
    TEST_TICKER_TEST,
)


def create_sample_dataframe() -> pd.DataFrame:
    """Create a sample DataFrame with stock data for testing."""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=SAMPLE_DAYS_LOOKBACK),
        end=datetime.now(),
        freq=SAMPLE_DATE_FREQUENCY,
    )

    data = {
        OPEN_COLUMN: [
            SAMPLE_BASE_OPEN + i * SAMPLE_VALUE_INCREMENT for i in range(len(dates))
        ],
        HIGH_COLUMN: [
            SAMPLE_BASE_HIGH + i * SAMPLE_VALUE_INCREMENT for i in range(len(dates))
        ],
        LOW_COLUMN: [
            SAMPLE_BASE_LOW + i * SAMPLE_VALUE_INCREMENT for i in range(len(dates))
        ],
        CLOSE_COLUMN: [
            SAMPLE_BASE_CLOSE + i * SAMPLE_VALUE_INCREMENT for i in range(len(dates))
        ],
        VOLUME_COLUMN: [
            SAMPLE_BASE_VOLUME + i * SAMPLE_VOLUME_INCREMENT for i in range(len(dates))
        ],
    }

    df = pd.DataFrame(data, index=dates)
    df.index.name = DATE_COLUMN
    return df


SAMPLE_TICKER = TEST_TICKER_TEST
VANGUARD_TEST_FUNDS = ["VTI", "VXUS", "BND"]
