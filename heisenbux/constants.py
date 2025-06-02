"""Constants used throughout the heisenbux package."""

from enum import StrEnum


class Directories(StrEnum):
    """Directory paths used in the application."""
    CACHE = "cache"
    GRAPHS = "graphs"


class FileExtensions(StrEnum):
    """File extensions used in the application."""
    CSV = ".csv"
    PNG = ".png"


class DataFrameColumns(StrEnum):
    """DataFrame column names for stock data."""
    CLOSE = "Close"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    VOLUME = "Volume"
    DATE = "Date"


class CLIOptions(StrEnum):
    """Command-line interface options."""
    NO_SHOW_PLOT = "--no-show-plot"
    NO_FORCE_DOWNLOAD = "--no-force-download"
    SHOW_PLOT = "--show-plot"
    FORCE_DOWNLOAD = "--force-download"


# Default values
DEFAULT_DAYS_LOOKBACK = 365

# Plot configuration
FIGURE_SIZE = (12, 6)
X_AXIS_ROTATION = 45
CLOSING_PRICE_LABEL = "Closing Price"
PRICE_USD_LABEL = "Price (USD)"
CLOSING_PRICES_TITLE_SUFFIX = " Closing Prices (Last Year)"
PLOT_SUFFIX = "_plot.png"

# Derived constants
ALL_PRICE_COLUMNS = [
    DataFrameColumns.OPEN.value,
    DataFrameColumns.HIGH.value,
    DataFrameColumns.LOW.value,
    DataFrameColumns.CLOSE.value,
    DataFrameColumns.VOLUME.value,
]

# CLI commands and options
POETRY_RUN_HEISENBUX = ["poetry", "run", "heisenbux"]

# Exit codes
EXIT_ERROR = 1
EXIT_USAGE_ERROR = 2
