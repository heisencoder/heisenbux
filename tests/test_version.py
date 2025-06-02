"""Test version information."""

from heisenbux import __version__


def test_version() -> None:
    """Test that version string is correctly formatted (X.Y.Z)."""
    import re

    # Version should match semantic versioning format
    version_pattern = r"^\d+\.\d+\.\d+$"
    assert re.match(
        version_pattern, __version__
    ), f"Version '{__version__}' does not match X.Y.Z format"
