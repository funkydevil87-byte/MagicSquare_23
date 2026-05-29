"""Locates empty cells in a partial magic square grid."""

from __future__ import annotations

from entity.value_objects.cell_coordinate import CellCoordinate
from entity.value_objects.empty_cell_pair import EmptyCellPair
from entity.value_objects.magic_constant import GridSize


class EmptyCellLocator:
    """Finds the two empty cells in row-major order (I6)."""

    def locate(self, grid: list[list[int]]) -> EmptyCellPair:
        """Return the first and second empty cell coordinates in scan order.

        Args:
            grid: 4×4 grid with exactly two ``0`` cells (caller precondition).

        Returns:
            EmptyCellPair with 1-index ``first`` and ``second`` coordinates.
        """
        empty_cells: list[CellCoordinate] = []
        for row_index in range(GridSize.VALUE):
            for col_index in range(GridSize.VALUE):
                if grid[row_index][col_index] == 0:
                    empty_cells.append(
                        CellCoordinate(row=row_index + 1, col=col_index + 1)
                    )
        return EmptyCellPair(first=empty_cells[0], second=empty_cells[1])
