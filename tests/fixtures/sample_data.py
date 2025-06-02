"""Sample data fixtures for testing."""

from datetime import datetime, timedelta

import pandas as pd

from heisenbux import constants
from tests import constants as test_constants


def create_sample_dataframe() -> pd.DataFrame:
    """Create a sample DataFrame with stock data for testing."""
    dates = pd.date_range(
        start=datetime.now()
        - timedelta(days=test_constants.SAMPLE_DAYS_LOOKBACK),
        end=datetime.now(),
        freq=test_constants.SAMPLE_DATE_FREQUENCY,
    )

    data = {
        constants.DataFrameColumns.OPEN: [
            test_constants.SAMPLE_BASE_OPEN + i * test_constants.SAMPLE_VALUE_INCREMENT
            for i in range(len(dates))
        ],
        constants.DataFrameColumns.HIGH: [
            test_constants.SAMPLE_BASE_HIGH + i * test_constants.SAMPLE_VALUE_INCREMENT
            for i in range(len(dates))
        ],
        constants.DataFrameColumns.LOW: [
            test_constants.SAMPLE_BASE_LOW + i * test_constants.SAMPLE_VALUE_INCREMENT
            for i in range(len(dates))
        ],
        constants.DataFrameColumns.CLOSE: [
            test_constants.SAMPLE_BASE_CLOSE + i * test_constants.SAMPLE_VALUE_INCREMENT
            for i in range(len(dates))
        ],
        constants.DataFrameColumns.VOLUME: [
            test_constants.SAMPLE_BASE_VOLUME
            + i * test_constants.SAMPLE_VOLUME_INCREMENT
            for i in range(len(dates))
        ],
    }

    df = pd.DataFrame(data, index=dates)
    df.index.name = constants.DataFrameColumns.DATE
    return df


SAMPLE_TICKER = test_constants.TestTickers.TEST
VANGUARD_TEST_FUNDS = ["VTI", "VXUS", "BND"]
