from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from magicsquare.boundary.schemas import (
    DUPLICATE_VALUE_CODE,
    DUPLICATE_VALUE_MESSAGE,
    INVALID_COL_COUNT_CODE,
    INVALID_COL_COUNT_MESSAGE,
    INVALID_EMPTY_COUNT_CODE,
    INVALID_EMPTY_COUNT_MESSAGE,
    INVALID_ROW_COUNT_CODE,
    INVALID_ROW_COUNT_MESSAGE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    NULL_INPUT_CODE,
    NULL_INPUT_MESSAGE,
    OUT_OF_RANGE_CODE,
    OUT_OF_RANGE_MESSAGE,
    FailureResult,
)

PRD_INVALID_SIZE_CODE = INVALID_SIZE_CODE
PRD_INVALID_SIZE_MESSAGE = INVALID_SIZE_MESSAGE

RESOLVE_PATCH = "magicsquare.control.magic_square_solver.MagicSquareSolver.resolve"
EXECUTE_PATCH = (
    "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
)

GRID_3X4: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_EMPTY_COLS: list[list[int]] = [[]] * 4

GRID_4X3: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

GRID_5X5: list[list[int]] = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 1, 2, 3, 4],
    [5, 6, 7, 8, 9],
]

GRID_NO_BLANKS: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

GRID_THREE_BLANKS: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 0, 0, 12],
    [4, 15, 14, 1],
]

GRID_MINUS_ONE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, -1, 12],
    [4, 15, 14, 1],
]

GRID_SEVENTEEN: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 17, 12],
    [4, 15, 14, 1],
]

GRID_DUPLICATE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 3, 12],
    [4, 15, 14, 1],
]

__all__ = [
    "DUPLICATE_VALUE_CODE",
    "DUPLICATE_VALUE_MESSAGE",
    "EXECUTE_PATCH",
    "FailureResult",
    "GRID_3X4",
    "GRID_4X3",
    "GRID_5X5",
    "GRID_DUPLICATE",
    "GRID_EMPTY_COLS",
    "GRID_MINUS_ONE",
    "GRID_NO_BLANKS",
    "GRID_SEVENTEEN",
    "GRID_THREE_BLANKS",
    "INVALID_COL_COUNT_CODE",
    "INVALID_COL_COUNT_MESSAGE",
    "INVALID_EMPTY_COUNT_CODE",
    "INVALID_EMPTY_COUNT_MESSAGE",
    "INVALID_ROW_COUNT_CODE",
    "INVALID_ROW_COUNT_MESSAGE",
    "NULL_INPUT_CODE",
    "NULL_INPUT_MESSAGE",
    "OUT_OF_RANGE_CODE",
    "OUT_OF_RANGE_MESSAGE",
    "PRD_INVALID_SIZE_CODE",
    "PRD_INVALID_SIZE_MESSAGE",
    "RESOLVE_PATCH",
]


if TYPE_CHECKING:
    from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary


@pytest.fixture
def boundary() -> MagicSquareBoundary:
    from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary

    return MagicSquareBoundary()
