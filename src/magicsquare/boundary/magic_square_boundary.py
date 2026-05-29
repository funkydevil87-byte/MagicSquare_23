"""Public Boundary API for partial magic square solving."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResult


class MagicSquareBoundary:
    """Adapter that validates input and orchestrates solve on valid grids."""

    def __init__(self) -> None:
        self._validator = InputValidator()

    def solve(self, grid: Any) -> FailureResult | Any:
        failure = self._validator.validate(grid)
        if failure is not None:
            return failure
        raise NotImplementedError
