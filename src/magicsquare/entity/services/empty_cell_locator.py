"""Locate blank cells in row-major order."""

from __future__ import annotations

from magicsquare.entity.constants import GRID_SIZE


class EmptyCellLocator:
    """Find the first and second blank cells using row-major scan."""

    def locate(self, grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return 1-indexed coordinates for the first and second blank cells.

        Args:
            grid: 4x4 grid with exactly two ``0`` cells.

        Returns:
            ``((r1, c1), (r2, c2))`` in 1-indexed coordinates.
        """
        blanks: list[tuple[int, int]] = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    blanks.append((row + 1, col + 1))
        first_blank, second_blank = blanks[0], blanks[1]
        return first_blank, second_blank
