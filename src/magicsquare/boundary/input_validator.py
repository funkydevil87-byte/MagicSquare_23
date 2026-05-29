"""Boundary input validation for grid contract violations."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.schemas import (
    GRID_SIZE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    FailureResult,
)


class InputValidator:
    """Validates grid shape before Control/Domain invocation."""

    def validate(self, grid: Any) -> FailureResult | None:
        if grid is None:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        if grid == []:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        if isinstance(grid, list) and len(grid) != GRID_SIZE:
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        if isinstance(grid, list) and any(len(row) != GRID_SIZE for row in grid):
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return None
