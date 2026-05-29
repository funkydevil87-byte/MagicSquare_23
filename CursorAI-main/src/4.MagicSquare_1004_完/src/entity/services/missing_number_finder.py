"""Finds missing numbers from a partial magic square grid."""

from __future__ import annotations

from entity.value_objects.magic_constant import CellValueRange
from entity.value_objects.missing_number_pair import MissingNumberPair


class MissingNumberFinder:
    """Determines which two values from {1..16} are absent (I7, I11)."""

    def find(self, grid: list[list[int]]) -> MissingNumberPair:
        """Return the two missing non-zero values in ascending order.

        Args:
            grid: 4×4 grid; ``0`` marks empty cells and is not a missing value.

        Returns:
            MissingNumberPair with ``smaller`` and ``larger`` missing integers.
        """
        present = {
            cell
            for row in grid
            for cell in row
            if cell != 0
        }
        missing = [
            value
            for value in range(CellValueRange.MIN, CellValueRange.MAX + 1)
            if value not in present
        ]
        return MissingNumberPair(smaller=missing[0], larger=missing[1])
