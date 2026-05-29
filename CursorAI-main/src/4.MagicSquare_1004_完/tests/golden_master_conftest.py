"""Pytest hooks and fixtures for Golden Master approve mode."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.golden_master_support import DEFAULT_GOLDEN_MASTER_PATH


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register ``--approve-golden`` CLI flag for baseline refresh."""
    parser.addoption(
        "--approve-golden",
        action="store_true",
        default=False,
        help="Overwrite golden master baseline with current solver output.",
    )


@pytest.fixture
def approve_golden(request: pytest.FixtureRequest) -> bool:
    """True when ``--approve-golden`` is passed on the pytest command line."""
    return bool(request.config.getoption("--approve-golden"))


@pytest.fixture
def golden_master_path() -> Path:
    """Path to the GM-1 baseline file."""
    return DEFAULT_GOLDEN_MASTER_PATH
