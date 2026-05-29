"""Validate complete 4x4 magic squares."""

from __future__ import annotations

import copy

from magicsquare.entity.constants import (
    CELL_MAX,
    CELL_MIN,
    GRID_SIZE,
    LINE_COUNT,
    MAGIC_CONSTANT,
)
from magicsquare.entity.validation_result import ValidationResult


class MagicSquareValidator:
    """Check the ten line sums and 1..16 uniqueness on complete grids."""

    def validate_complete(self, grid: list[list[int]]) -> ValidationResult:
        """Return whether ``grid`` is a valid complete magic square.

        Args:
            grid: 4x4 grid without blank cells.

        Returns:
            ``ValidationResult`` with ``valid=True`` only when all invariants hold.
        """
        if not self._is_complete_unique_grid(grid):
            return ValidationResult(valid=False)
        if not self._all_line_sums_equal_magic_constant(grid):
            return ValidationResult(valid=False)
        return ValidationResult(valid=True)

    def _is_complete_unique_grid(self, grid: list[list[int]]) -> bool:
        values = [grid[row][col] for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
        if 0 in values:
            return False
        if len(set(values)) != CELL_MAX:
            return False
        return set(values) == set(range(CELL_MIN, CELL_MAX + 1))

    def _all_line_sums_equal_magic_constant(self, grid: list[list[int]]) -> bool:
        line_sums = self._line_sums(grid)
        return len(line_sums) == LINE_COUNT and all(
            total == MAGIC_CONSTANT for total in line_sums
        )

    def _line_sums(self, grid: list[list[int]]) -> list[int]:
        sums: list[int] = []
        for row in range(GRID_SIZE):
            sums.append(sum(grid[row][col] for col in range(GRID_SIZE)))
        for col in range(GRID_SIZE):
            sums.append(sum(grid[row][col] for row in range(GRID_SIZE)))
        sums.append(sum(grid[index][index] for index in range(GRID_SIZE)))
        sums.append(sum(grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)))
        return sums

    def complete_grid(
        self,
        partial: list[list[int]],
        first_blank: tuple[int, int],
        second_blank: tuple[int, int],
        first_value: int,
        second_value: int,
    ) -> list[list[int]]:
        """Return a copy of ``partial`` with the two blanks filled.

        Args:
            partial: Source partial grid.
            first_blank: 1-indexed first blank coordinate.
            second_blank: 1-indexed second blank coordinate.
            first_value: Value for the first blank.
            second_value: Value for the second blank.

        Returns:
            New grid with both blanks filled.
        """
        completed = copy.deepcopy(partial)
        r1, c1 = first_blank
        r2, c2 = second_blank
        completed[r1 - 1][c1 - 1] = first_value
        completed[r2 - 1][c2 - 1] = second_value
        return completed
