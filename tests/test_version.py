"""Test version information."""

from heisenbux import __version__


def test_version():
    """Test that version information is correct."""
    assert __version__ == "0.1.0"
