"""Public Boundary API for partial magic square solving."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.exceptions import BoundaryValidationError, UnsolvableError
from magicsquare.boundary.input_validator import InputValidator
from magicsquare.control.exceptions import SolveUnsolvableError
from magicsquare.control.magic_square_solver import MagicSquareSolver


class MagicSquareBoundary:
    """Adapter that validates input and orchestrates solve on valid grids."""

    def __init__(self) -> None:
        self._validator = InputValidator()
        self._solver = MagicSquareSolver()

    def solve(self, grid: Any) -> list[int]:
        """Validate input and solve when the grid contract is satisfied.

        Args:
            grid: Raw 4x4 integer matrix input.

        Returns:
            ``[r1, c1, n1, r2, c2, n2]`` on success.

        Raises:
            BoundaryValidationError: When input validation fails (E001~E005).
            UnsolvableError: When both solve attempts fail (E006).
        """
        failure = self._validator.validate(grid)
        if failure is not None:
            raise BoundaryValidationError(failure.code, failure.message)
        try:
            return self._solver.resolve(grid)
        except SolveUnsolvableError:
            raise UnsolvableError from None
