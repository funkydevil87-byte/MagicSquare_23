"""Public Boundary API for partial magic square solving."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.exceptions import UnsolvableError
from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResult
from magicsquare.control.magic_square_solver import MagicSquareSolver
from magicsquare.entity.exceptions import UnsolvableDomainError


class MagicSquareBoundary:
    """Adapter that validates input and orchestrates solve on valid grids."""

    def __init__(self) -> None:
        self._validator = InputValidator()
        self._solver = MagicSquareSolver()

    def solve(self, grid: Any) -> FailureResult | list[int]:
        """Validate input and solve when the grid contract is satisfied.

        Args:
            grid: Raw 4x4 integer matrix input.

        Returns:
            ``FailureResult`` on validation failure or ``list[int]`` on success.

        Raises:
            UnsolvableError: When both solve attempts fail.
        """
        failure = self._validator.validate(grid)
        if failure is not None:
            return failure
        try:
            return self._solver.resolve(grid)
        except UnsolvableDomainError:
            raise UnsolvableError from None
