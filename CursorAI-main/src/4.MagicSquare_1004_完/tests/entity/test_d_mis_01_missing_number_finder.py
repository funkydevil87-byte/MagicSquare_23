"""Report/09 Track B — D-MIS-01 missing number finder RED skeleton.

G1 누락 숫자 2개 오름차순. Domain Mock 금지. AC-FR03-*.
"""

from __future__ import annotations

import pytest

from entity.services.missing_number_finder import MissingNumberFinder

# Report/02 G1 — missing {7,10}
# grid_g1 = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]


class TestMissingNumberFinder:
    """D-MIS-01 — 누락 숫자 2개 오름차순."""

    def test_d_mis_01_g1_returns_sorted_missing_pair(self) -> None:
        """D-MIS-01, I7, I11 — G1 (smaller,larger)==(7,10)."""
        # D-MIS-01
        # Given
        finder = MissingNumberFinder()
        grid = [[16, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]

        # When
        result = finder.find(grid)

        # Then
        assert (result.smaller, result.larger) == (7, 10)
