from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pydantic import BaseModel

PRD_INVALID_SIZE_CODE = "INVALID_SIZE"
PRD_INVALID_SIZE_MESSAGE = "Grid must be 4x4."

RESOLVE_PATCH = "magicsquare.control.magic_square_solver.MagicSquareSolver.resolve"

GRID_3X4: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_EMPTY_COLS: list[list[int]] = [[]] * 4


class FailureResult(BaseModel):
    """Expected failure payload contract for AC-FR-01-01 RED tests."""

    code: str
    message: str


if TYPE_CHECKING:
    from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary


@pytest.fixture
def boundary() -> MagicSquareBoundary:
    from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary

    return MagicSquareBoundary()
