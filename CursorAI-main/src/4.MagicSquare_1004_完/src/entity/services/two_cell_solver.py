"""Solves partial magic squares by trying Step A then Step B (I8~I10)."""

from __future__ import annotations

import copy

from entity.exceptions.domain_errors import UnsolvableDomainError
from entity.services.empty_cell_locator import EmptyCellLocator
from entity.services.magic_square_validator import MagicSquareValidator
from entity.services.missing_number_finder import MissingNumberFinder
from entity.value_objects.solution_result import SolutionResult


class TwoCellSolver:
    """Attempts smaller-first then reverse placement for two empty cells."""

    def __init__(
        self,
        empty_cell_locator: EmptyCellLocator | None = None,
        missing_number_finder: MissingNumberFinder | None = None,
        magic_square_validator: MagicSquareValidator | None = None,
    ) -> None:
        """Initialize solver with optional domain service dependencies.

        Args:
            empty_cell_locator: Locates empty cells; defaults to new instance.
            missing_number_finder: Finds missing values; defaults to new instance.
            magic_square_validator: Validates complete grids; defaults to new.
        """
        self._empty_cell_locator = empty_cell_locator or EmptyCellLocator()
        self._missing_number_finder = missing_number_finder or MissingNumberFinder()
        self._magic_square_validator = (
            magic_square_validator or MagicSquareValidator()
        )

    def solve(self, grid: list[list[int]]) -> SolutionResult:
        """Find a valid completion using Step A, then Step B if needed.

        Args:
            grid: Partial 4×4 grid with exactly two empty cells.

        Returns:
            SolutionResult with ``[r1, c1, n1, r2, c2, n2]`` on success.

        Raises:
            UnsolvableDomainError: When both combinations fail validation.
        """
        empty_cells = self._empty_cell_locator.locate(grid)
        missing_numbers = self._missing_number_finder.find(grid)
        first = empty_cells.first
        second = empty_cells.second
        smaller = missing_numbers.smaller
        larger = missing_numbers.larger

        step_a = self._try_placement(
            grid,
            first.row,
            first.col,
            smaller,
            second.row,
            second.col,
            larger,
        )
        if step_a is not None:
            return step_a

        step_b = self._try_placement(
            grid,
            first.row,
            first.col,
            larger,
            second.row,
            second.col,
            smaller,
        )
        if step_b is not None:
            return step_b

        raise UnsolvableDomainError("No valid magic square completion")

    def _try_placement(
        self,
        grid: list[list[int]],
        first_row: int,
        first_col: int,
        first_value: int,
        second_row: int,
        second_col: int,
        second_value: int,
    ) -> SolutionResult | None:
        """Fill two cells and validate; return result or None if invalid."""
        candidate = copy.deepcopy(grid)
        candidate[first_row - 1][first_col - 1] = first_value
        candidate[second_row - 1][second_col - 1] = second_value
        if not self._magic_square_validator.is_valid_complete(candidate):
            return None
        return SolutionResult(
            values=[
                first_row,
                first_col,
                first_value,
                second_row,
                second_col,
                second_value,
            ]
        )
