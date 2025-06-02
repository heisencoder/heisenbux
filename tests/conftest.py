"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from tests.helpers import temp_directory  # noqa: F401

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(autouse=True)
def reset_matplotlib() -> None:
    """Reset matplotlib state between tests to avoid interference."""
    plt.close("all")


@pytest.fixture
def disable_network_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    """Disable network calls for unit tests."""

    def mock_urlopen(*args: object, **kwargs: object) -> None:
        raise RuntimeError("Network access not allowed in unit tests")

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen)
