"""Boundary input validation for grid contract violations."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.schemas import (
    DUPLICATE_VALUE_CODE,
    DUPLICATE_VALUE_MESSAGE,
    GRID_SIZE,
    INVALID_COL_COUNT_CODE,
    INVALID_COL_COUNT_MESSAGE,
    INVALID_EMPTY_COUNT_CODE,
    INVALID_EMPTY_COUNT_MESSAGE,
    INVALID_ROW_COUNT_CODE,
    INVALID_ROW_COUNT_MESSAGE,
    NULL_INPUT_CODE,
    NULL_INPUT_MESSAGE,
    OUT_OF_RANGE_CODE,
    OUT_OF_RANGE_MESSAGE,
    FailureResult,
)


class InputValidator:
    """Validates grid shape and cell contract before Control/Domain invocation."""

    def validate(self, grid: Any) -> FailureResult | None:
        if grid is None:
            return FailureResult(code=NULL_INPUT_CODE, message=NULL_INPUT_MESSAGE)

        if not isinstance(grid, list):
            return FailureResult(
                code=INVALID_ROW_COUNT_CODE,
                message=INVALID_ROW_COUNT_MESSAGE,
            )

        if len(grid) != GRID_SIZE:
            return FailureResult(
                code=INVALID_ROW_COUNT_CODE,
                message=INVALID_ROW_COUNT_MESSAGE,
            )

        for row in grid:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                return FailureResult(
                    code=INVALID_COL_COUNT_CODE,
                    message=INVALID_COL_COUNT_MESSAGE,
                )

        blank_count = 0
        seen_nonzero: set[int] = set()

        for row in grid:
            for value in row:
                if not isinstance(value, int):
                    return FailureResult(
                        code=OUT_OF_RANGE_CODE,
                        message=OUT_OF_RANGE_MESSAGE,
                    )
                if value == 0:
                    blank_count += 1
                    continue
                if value < 0 or value > 16:
                    return FailureResult(
                        code=OUT_OF_RANGE_CODE,
                        message=OUT_OF_RANGE_MESSAGE,
                    )
                if value in seen_nonzero:
                    return FailureResult(
                        code=DUPLICATE_VALUE_CODE,
                        message=DUPLICATE_VALUE_MESSAGE,
                    )
                seen_nonzero.add(value)

        if blank_count != 2:
            return FailureResult(
                code=INVALID_EMPTY_COUNT_CODE,
                message=INVALID_EMPTY_COUNT_MESSAGE,
            )

        return None
