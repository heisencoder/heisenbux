"""Command line interface for Heisenbux."""

import click
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

from heisenbux import plot



@click.command()
@click.argument('ticker')
@click.option('--show-plot/--no-show-plot', default=True,
              help='Whether to display the price plot (default: True)')
@click.option('--force-download/--no-force-download', default=False,
              help='Force download new data even if cached (default: False)')
def main(ticker: str, show_plot: bool, force_download: bool):
    """Fetch the last year of daily price data for a given stock ticker and save it to a CSV file.

    TICKER: The stock ticker symbol (e.g., AAPL, GOOGL)
    """
    # Create output directories if they don't exist
    cache_dir = Path('cache')
    graphs_dir = Path('graphs')
    cache_dir.mkdir(parents=True, exist_ok=True)
    graphs_dir.mkdir(parents=True, exist_ok=True)

    # Check for cached data
    cache_file = cache_dir / f"{ticker.upper()}.csv"

    if cache_file.exists() and not force_download:
        click.echo(f"Using cached data from {cache_file}")
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
    else:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        # Fetch data
        click.echo(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            click.echo(f"No data found for ticker {ticker}", err=True)
            return

        # Save to CSV in cache directory
        df.to_csv(cache_file)
        click.echo(f"Data saved to {cache_file}")

    if show_plot:
        plot.save_plot(df, ticker, graphs_dir)


if __name__ == '__main__':
    main()
