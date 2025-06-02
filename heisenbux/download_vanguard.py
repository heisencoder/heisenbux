"""Script to download data for popular Vanguard funds."""

import sys

import click

from heisenbux import cli, constants


def _run_heisenbux_for_ticker(ticker: str, show_plot: bool = True, force_download: bool = False) -> None:
    """Run heisenbux for a specific ticker.

    Args:
        ticker: Stock ticker symbol
        show_plot: Whether to show the plot
        force_download: Whether to force download
    """
    # Save original argv
    original_argv = sys.argv
    try:
        # Set up argv for click
        args = [sys.argv[0], ticker]
        if not show_plot:
            args.append(constants.CLIOptions.NO_SHOW_PLOT)
        if force_download:
            args.append(constants.CLIOptions.FORCE_DOWNLOAD)
        
        sys.argv = args
        cli.main(standalone_mode=False)
    except (SystemExit, click.Abort):
        pass  # Click raises SystemExit on success or Abort on error
    finally:
        # Restore original argv
        sys.argv = original_argv


def download_funds(funds: list[str]) -> None:
    """Download data for a list of Vanguard funds."""
    for fund in funds:
        print(f"\nDownloading data for {fund}...")
        _run_heisenbux_for_ticker(fund, show_plot=False, force_download=False)


def generate_plots(funds: list[str]) -> None:
    """Generate plots for a list of Vanguard funds."""
    for fund in funds:
        print(f"\nGenerating plot for {fund}...")
        _run_heisenbux_for_ticker(fund, show_plot=True, force_download=False)


if __name__ == "__main__":
    vanguard_funds: list[str] = [
        "VTI",  # Vanguard Total Stock Market ETF
        "VOO",  # Vanguard S&P 500 ETF
        "VXUS",  # Vanguard Total International Stock ETF
        "BND",  # Vanguard Total Bond Market ETF
        "VNQ",  # Vanguard Real Estate ETF
        "VGT",  # Vanguard Information Technology ETF
        "VYM",  # Vanguard High Dividend Yield ETF
        "VUG",  # Vanguard Growth ETF
        "VB",  # Vanguard Small-Cap ETF
        "VTV",  # Vanguard Value ETF
    ]

    # First ensure all data is downloaded
    download_funds(vanguard_funds)
    print("\nAll downloads completed!")

    # Then generate plots for all funds
    print("\nGenerating plots for all funds...")
    generate_plots(vanguard_funds)
    print("\nAll plots generated!")
