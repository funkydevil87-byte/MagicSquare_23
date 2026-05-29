"""Control-layer orchestration for partial magic square solving."""

from __future__ import annotations

import copy

from magicsquare.entity.exceptions import UnsolvableDomainError
from magicsquare.entity.services.empty_cell_locator import EmptyCellLocator
from magicsquare.entity.services.missing_number_finder import MissingNumberFinder
from magicsquare.entity.services.two_cell_solver import TwoCellSolver


class SolvePartialMagicSquare:
    """Orchestrate Attempt 1/2 and return the solution vector."""

    def __init__(self) -> None:
        self._locator = EmptyCellLocator()
        self._missing_finder = MissingNumberFinder()
        self._two_cell_solver = TwoCellSolver()

    def execute(self, grid: list[list[int]]) -> list[int]:
        """Solve a validated partial grid.

        Args:
            grid: 4x4 partial grid that passed Boundary validation.

        Returns:
            ``[r1, c1, n1, r2, c2, n2]`` with 1-indexed coordinates.

        Raises:
            UnsolvableDomainError: When neither attempt yields a magic square.
        """
        working_grid = copy.deepcopy(grid)
        first_blank, second_blank = self._locator.locate(working_grid)
        small, large = self._missing_finder.find_missing(working_grid)

        attempt_one = self._two_cell_solver.attempt(
            working_grid,
            first_blank,
            second_blank,
            small,
            large,
        )
        if attempt_one is not None:
            return attempt_one

        attempt_two = self._two_cell_solver.attempt(
            working_grid,
            first_blank,
            second_blank,
            large,
            small,
        )
        if attempt_two is not None:
            return attempt_two

        raise UnsolvableDomainError
