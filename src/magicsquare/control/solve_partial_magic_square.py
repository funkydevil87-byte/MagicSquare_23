"""Control-layer orchestration for partial magic square solving."""

from __future__ import annotations

import copy
from typing import Any

from magicsquare.entity.exceptions import UnsolvableDomainError
from magicsquare.entity.services.empty_cell_locator import EmptyCellLocator
from magicsquare.entity.services.magic_square_validator import MagicSquareValidator
from magicsquare.entity.services.missing_number_finder import MissingNumberFinder


class SolvePartialMagicSquare:
    """Orchestrate Attempt 1/2 and return the solution vector."""

    def __init__(self) -> None:
        self._locator = EmptyCellLocator()
        self._missing_finder = MissingNumberFinder()
        self._validator = MagicSquareValidator()

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

        attempt_one = self._attempt(
            working_grid,
            first_blank,
            second_blank,
            small,
            large,
        )
        if attempt_one is not None:
            return attempt_one

        attempt_two = self._attempt(
            working_grid,
            first_blank,
            second_blank,
            large,
            small,
        )
        if attempt_two is not None:
            return attempt_two

        raise UnsolvableDomainError

    def _attempt(
        self,
        partial: list[list[int]],
        first_blank: tuple[int, int],
        second_blank: tuple[int, int],
        first_value: int,
        second_value: int,
    ) -> list[int] | None:
        completed = self._validator.complete_grid(
            partial,
            first_blank,
            second_blank,
            first_value,
            second_value,
        )
        if not self._validator.validate_complete(completed).valid:
            return None

        r1, c1 = first_blank
        r2, c2 = second_blank
        return [r1, c1, first_value, r2, c2, second_value]
