"""D-LOC-01 — locate blank cells. Track B Entity RED skeleton (no Domain mock)."""

from __future__ import annotations

import pytest


class TestDLoc01:
    """FR-02 / I6 — row-major first and second blank on G1."""

    def test_d_loc_01_g1_row_major_blank_pair(self) -> None:
        # D-LOC-01
        # from magicsquare.entity.services.empty_cell_locator import EmptyCellLocator
        # Given: G1 partial grid (blanks at (2,2) and (3,3) 1-index)
        # locator = EmptyCellLocator()
        # When: locator.locate(grid_g1)
        pytest.fail("RED: D-LOC-01 — G1 blanks (2,2) and (3,3) row-major order")
