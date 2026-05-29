"""Pair of empty cell coordinates in row-major scan order."""

from __future__ import annotations

from dataclasses import dataclass

from entity.value_objects.cell_coordinate import CellCoordinate


@dataclass(frozen=True)
class EmptyCellPair:
    """Two empty cells discovered in row-major order.

    Attributes:
        first: First empty cell coordinate (1-index).
        second: Second empty cell coordinate (1-index).
    """

    first: CellCoordinate
    second: CellCoordinate
