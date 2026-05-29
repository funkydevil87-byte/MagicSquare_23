"""Fixtures for Screen characterization tests (headless, no tkinter root)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from magicsquare.boundary.screen.app import MagicSquareApp
from magicsquare.entity.constants import GRID_SIZE


class _MockStringVar:
    """Minimal StringVar stand-in for headless Screen tests."""

    def __init__(self, value: str = "") -> None:
        self._value = value

    def get(self) -> str:
        return self._value

    def set(self, value: str) -> None:
        self._value = value


def _make_minimal_app() -> MagicSquareApp:
    """Build MagicSquareApp without ``_build_layout`` (CI-safe, no tk root)."""
    app = MagicSquareApp.__new__(MagicSquareApp)
    app._root = None
    app._boundary = MagicSquareBoundary()
    app._cell_vars = [
        [_MockStringVar("") for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]
    app._result_var = _MockStringVar("")
    app._result_label = MagicMock()
    return app


@pytest.fixture
def app() -> MagicSquareApp:
    return _make_minimal_app()


def assert_label_foreground(app: MagicSquareApp, expected: str) -> None:
    """Assert the last ``configure`` call set ``foreground`` on the result label."""
    calls = app._result_label.configure.call_args_list
    assert calls, "expected _result_label.configure to be called"
    last_kwargs = calls[-1].kwargs
    assert last_kwargs.get("foreground") == expected
