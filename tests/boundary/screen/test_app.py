"""RF-01 — Screen characterization tests for MagicSquareApp."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from magicsquare.boundary.exceptions import BoundaryValidationError, UnsolvableError
from magicsquare.boundary.screen.app import MagicSquareApp, SAMPLE_G1
from magicsquare.entity.constants import GRID_SIZE
from tests.boundary.screen.conftest import assert_label_foreground


class TestReadGrid:
    """RF-01-01 — _read_grid() parses StringVar cells."""

    def test_blank_cell_becomes_zero(self, app: MagicSquareApp) -> None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                app._cell_vars[row][col].set("")
        grid = app._read_grid()
        assert grid == [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    def test_numeric_cell_parsed(self, app: MagicSquareApp) -> None:
        app._cell_vars[0][0].set("16")
        grid = app._read_grid()
        assert grid[0][0] == 16

    def test_non_integer_raises_value_error(self, app: MagicSquareApp) -> None:
        app._cell_vars[1][1].set("abc")
        with pytest.raises(ValueError, match="Cell \\(2,2\\)"):
            app._read_grid()

    def test_out_of_range_raises_value_error(self, app: MagicSquareApp) -> None:
        app._cell_vars[0][0].set("17")
        with pytest.raises(ValueError, match="0–16"):
            app._read_grid()

    def test_negative_raises_value_error(self, app: MagicSquareApp) -> None:
        app._cell_vars[0][0].set("-1")
        with pytest.raises(ValueError, match="0–16"):
            app._read_grid()


class TestDisplayResult:
    """RF-01-02 / RF-05-02 — _display_result() delegates to ResultFormatter."""

    def test_success_vector_shows_coordinates(self, app: MagicSquareApp) -> None:
        app._display_result([2, 2, 10, 3, 3, 7])
        text = app._result_var.get()
        assert "Solve succeeded" in text
        assert "blank (2,2) ← 10" in text
        assert "[2, 2, 10, 3, 3, 7]" in text
        assert_label_foreground(app, "#166534")

    def test_unknown_result_uses_warning_tone(self, app: MagicSquareApp) -> None:
        app._display_result({"unexpected": True})
        text = app._result_var.get()
        assert "Unknown result type" in text
        assert_label_foreground(app, "#92400e")


class TestOnSolve:
    """RF-01-03 — on_solve() delegates to Boundary and routes outcomes."""

    @patch.object(MagicSquareApp, "_read_grid", return_value=[[0] * GRID_SIZE for _ in range(GRID_SIZE)])
    @patch.object(MagicSquareApp, "_display_result")
    def test_success_calls_display_result(
        self,
        display_mock: MagicMock,
        _read_mock: MagicMock,
        app: MagicSquareApp,
    ) -> None:
        app._boundary = MagicMock()
        app._boundary.solve.return_value = [1, 2, 3, 1, 4, 13]
        app.on_solve()
        app._boundary.solve.assert_called_once()
        display_mock.assert_called_once_with([1, 2, 3, 1, 4, 13])

    @patch.object(MagicSquareApp, "_read_grid", return_value=[[0] * GRID_SIZE for _ in range(GRID_SIZE)])
    def test_validation_error_shown_in_result(
        self,
        _read_mock: MagicMock,
        app: MagicSquareApp,
    ) -> None:
        app._boundary = MagicMock()
        app._boundary.solve.side_effect = BoundaryValidationError(
            "NULL_INPUT",
            "Input matrix must not be null.",
        )
        app.on_solve()
        text = app._result_var.get()
        assert "Boundary validation failed" in text
        assert "NULL_INPUT" in text
        assert_label_foreground(app, "#b91c1c")

    @patch.object(MagicSquareApp, "_read_grid", return_value=[[0] * GRID_SIZE for _ in range(GRID_SIZE)])
    def test_unsolvable_error_shown_in_result(
        self,
        _read_mock: MagicMock,
        app: MagicSquareApp,
    ) -> None:
        app._boundary = MagicMock()
        app._boundary.solve.side_effect = UnsolvableError()
        app.on_solve()
        text = app._result_var.get()
        assert "UNSOLVABLE" in text
        assert_label_foreground(app, "#b91c1c")

    def test_read_grid_value_error_shown_in_result(self, app: MagicSquareApp) -> None:
        app._cell_vars[0][0].set("bad")
        app.on_solve()
        text = app._result_var.get()
        assert "Cell (1,1)" in text
        assert_label_foreground(app, "#b91c1c")


class TestLoadGrid:
    """RF-01-04 — load_grid() maps 0 to blank display."""

    def test_zero_renders_as_empty_string(self, app: MagicSquareApp) -> None:
        app.load_grid(SAMPLE_G1)
        assert app._cell_vars[1][1].get() == ""
        assert app._cell_vars[2][2].get() == ""

    def test_nonzero_renders_as_string(self, app: MagicSquareApp) -> None:
        app.load_grid(SAMPLE_G1)
        assert app._cell_vars[0][0].get() == "16"
        assert app._cell_vars[3][3].get() == "1"
