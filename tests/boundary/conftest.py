from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from magicsquare.boundary.schemas import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    FailureResult,
)

PRD_INVALID_SIZE_CODE = INVALID_SIZE_CODE
PRD_INVALID_SIZE_MESSAGE = INVALID_SIZE_MESSAGE

RESOLVE_PATCH = "magicsquare.control.magic_square_solver.MagicSquareSolver.resolve"

GRID_3X4: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_EMPTY_COLS: list[list[int]] = [[]] * 4


if TYPE_CHECKING:
    from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary


@pytest.fixture
def boundary() -> MagicSquareBoundary:
    from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary

    return MagicSquareBoundary()
