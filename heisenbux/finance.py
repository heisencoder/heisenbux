"""Wrapper around yfinance with caching support"""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf


def get_ticker_data(ticker: str, force_download: bool = False) -> pd.DataFrame:
    """Fetch ticker data from yfinance with caching support.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        force_download: If True, download fresh data even if cached data exists

    Returns:
        DataFrame with stock data
        
    Raises:
        ValueError: If no data found for the ticker
        Exception: If there's an error fetching data
    """
    # Create output directories if they don't exist
    cache_dir = Path("cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Check for cached data
    cache_file = cache_dir / f"{ticker.upper()}.csv"

    if cache_file.exists() and not force_download:
        print(f"Using cached data from {cache_file}")
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
    else:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        # Fetch data
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            raise ValueError(f"No data found for ticker {ticker}")

        # Save to CSV in cache directory
        df.to_csv(cache_file)
        print(f"Data saved to {cache_file}")

    return df
