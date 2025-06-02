"""Constants used throughout the heisenbux package."""

# Directory paths
CACHE_DIR = "cache"
GRAPHS_DIR = "graphs"

# File extensions
CSV_EXTENSION = ".csv"
PNG_EXTENSION = ".png"
PLOT_SUFFIX = "_plot.png"

# Default values
DEFAULT_DAYS_LOOKBACK = 365

# DataFrame columns
CLOSE_COLUMN = "Close"
OPEN_COLUMN = "Open"
HIGH_COLUMN = "High"
LOW_COLUMN = "Low"
VOLUME_COLUMN = "Volume"
DATE_COLUMN = "Date"
ALL_PRICE_COLUMNS = [OPEN_COLUMN, HIGH_COLUMN, LOW_COLUMN, CLOSE_COLUMN, VOLUME_COLUMN]

# Plot configuration
FIGURE_SIZE = (12, 6)
X_AXIS_ROTATION = 45
CLOSING_PRICE_LABEL = "Closing Price"
PRICE_USD_LABEL = "Price (USD)"
CLOSING_PRICES_TITLE_SUFFIX = " Closing Prices (Last Year)"

# CLI commands and options
POETRY_RUN_HEISENBUX = ["poetry", "run", "heisenbux"]
NO_SHOW_PLOT_FLAG = "--no-show-plot"
NO_FORCE_DOWNLOAD_FLAG = "--no-force-download"
SHOW_PLOT_FLAG = "--show-plot"

# Exit codes
EXIT_ERROR = 1
EXIT_USAGE_ERROR = 2
