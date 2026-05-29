"""Boundary end-to-end tests for solve success and UNSOLVABLE."""

from __future__ import annotations

import pytest

from magicsquare.boundary.exceptions import UnsolvableError
from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from tests.conftest import GRID_G1, GRID_G3, GRID_TD01


class TestBoundaryE2E:
    """MagicSquareBoundary.solve() integration with Control/Entity."""

    def test_td01_small_first_success(self) -> None:
        boundary = MagicSquareBoundary()
        result = boundary.solve(GRID_TD01)
        assert result == [1, 2, 3, 1, 4, 13]

    def test_g1_reverse_success(self) -> None:
        boundary = MagicSquareBoundary()
        result = boundary.solve(GRID_G1)
        assert result == [2, 2, 10, 3, 3, 7]

    def test_g3_unsolvable_raises(self) -> None:
        boundary = MagicSquareBoundary()
        with pytest.raises(UnsolvableError) as exc_info:
            boundary.solve(GRID_G3)
        assert exc_info.value.code == "UNSOLVABLE"
