"""Report/09 Track B — D-LOC-01 empty cell locator RED skeleton.

G1 row-major 빈칸 2좌표 탐색. Domain Mock 금지. AC-FR02-*.
"""

from __future__ import annotations

import pytest

from entity.services.empty_cell_locator import EmptyCellLocator

# Report/02 G1 — (2,2)=0, (3,3)=0
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]


class TestEmptyCellLocator:
    """D-LOC-01 — row-major 빈칸 2좌표 탐색."""

    def test_d_loc_01_g1_returns_row_major_blank_coords(self) -> None:
        """D-LOC-01, I6 — G1 first=(2,2), second=(3,3)."""
        # D-LOC-01
        # Given
        locator = EmptyCellLocator()
        grid = [[16, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]

        # When
        result = locator.locate(grid)

        # Then
        assert (result.first.row, result.first.col) == (2, 2)
        assert (result.second.row, result.second.col) == (3, 3)
