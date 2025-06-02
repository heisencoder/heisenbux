"""Sample data fixtures for testing."""

from datetime import datetime, timedelta

import pandas as pd


def create_sample_dataframe() -> pd.DataFrame:
    """Create a sample DataFrame with stock data for testing."""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=30), end=datetime.now(), freq="D"
    )

    data = {
        "Open": [100.0 + i * 0.5 for i in range(len(dates))],
        "High": [101.0 + i * 0.5 for i in range(len(dates))],
        "Low": [99.0 + i * 0.5 for i in range(len(dates))],
        "Close": [100.5 + i * 0.5 for i in range(len(dates))],
        "Volume": [1000000 + i * 10000 for i in range(len(dates))],
    }

    df = pd.DataFrame(data, index=dates)
    df.index.name = "Date"
    return df


SAMPLE_TICKER = "TEST"
VANGUARD_TEST_FUNDS = ["VTI", "VXUS", "BND"]
