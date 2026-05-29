"""Validates complete 4×4 magic square invariants (I1~I5)."""

from __future__ import annotations

from entity.value_objects.magic_constant import CellValueRange, GridSize, MagicConstant


class MagicSquareValidator:
    """Checks whether a fully filled grid satisfies magic square rules."""

    def is_valid_complete(self, grid: list[list[int]]) -> bool:
        """Return True when the grid satisfies I1~I5 for a complete magic square.

        Args:
            grid: 4×4 grid with no empty cells.

        Returns:
            True if all row, column, diagonal sums equal ``MagicConstant`` and
            values are exactly ``{1..16}`` each once; otherwise False.
        """
        if any(cell == 0 for row in grid for cell in row):
            return False

        expected_values = set(
            range(CellValueRange.MIN, CellValueRange.MAX + 1)
        )
        if {cell for row in grid for cell in row} != expected_values:
            return False

        target = MagicConstant.VALUE
        for row in grid:
            if sum(row) != target:
                return False

        for col_index in range(GridSize.VALUE):
            if sum(grid[row_index][col_index] for row_index in range(GridSize.VALUE)) != target:
                return False

        main_diagonal = sum(
            grid[index][index] for index in range(GridSize.VALUE)
        )
        if main_diagonal != target:
            return False

        anti_diagonal = sum(
            grid[index][GridSize.VALUE - 1 - index]
            for index in range(GridSize.VALUE)
        )
        return anti_diagonal == target
