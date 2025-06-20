"""Command line interface for Heisenbux."""

import click

from heisenbux import constants, finance, plot


@click.command()
@click.argument("ticker")
@click.option(
    f"{constants.CLIOptions.SHOW_PLOT}/{constants.CLIOptions.NO_SHOW_PLOT}",
    default=True,
    help="Whether to display the price plot (default: True)",
)
@click.option(
    f"{constants.CLIOptions.FORCE_DOWNLOAD}/{constants.CLIOptions.NO_FORCE_DOWNLOAD}",
    default=False,
    help="Force download new data even if cached (default: False)",
)
def main(ticker: str, show_plot: bool, force_download: bool) -> None:
    """Fetch daily price data for a stock ticker and save it to a CSV file.

    Args:
        ticker: The stock ticker symbol (e.g., AAPL, GOOGL)
    """
    try:
        df = finance.get_ticker_data(ticker, force_download)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e

    if show_plot:
        plot.save_plot(df, ticker)


if __name__ == "__main__":
    main()
