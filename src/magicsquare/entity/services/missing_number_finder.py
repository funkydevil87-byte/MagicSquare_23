"""Find missing numbers from a partial grid."""

from __future__ import annotations

from magicsquare.entity.constants import CELL_MAX, CELL_MIN, GRID_SIZE


class MissingNumberFinder:
    """Compute the two missing values from ``1..16``."""

    def find_missing(self, grid: list[list[int]]) -> tuple[int, int]:
        """Return missing numbers as ``(min, max)``.

        Args:
            grid: 4x4 partial grid.

        Returns:
            Ascending pair of missing integers.
        """
        present = {
            grid[row][col]
            for row in range(GRID_SIZE)
            for col in range(GRID_SIZE)
            if grid[row][col] != 0
        }
        missing = [value for value in range(CELL_MIN, CELL_MAX + 1) if value not in present]
        return missing[0], missing[1]
