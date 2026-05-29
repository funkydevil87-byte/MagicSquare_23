"""U-IN-04 — value range violations (E004)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from magicsquare.boundary.exceptions import BoundaryValidationError
from magicsquare.boundary.input_validator import InputValidator
from tests.boundary.conftest import (
    EXECUTE_PATCH,
    GRID_MINUS_ONE,
    GRID_SEVENTEEN,
    OUT_OF_RANGE_CODE,
    OUT_OF_RANGE_MESSAGE,
    FailureResult,
)

GRID_BOOL_TRUE: list[list[int]] = [
    [True, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestUIn04Range:
    """FR-01 / AC-FR01-07 — OUT_OF_RANGE failure envelope."""

    def test_u_in_04a_minus_one_returns_e004(self) -> None:
        validator = InputValidator()
        result = validator.validate(GRID_MINUS_ONE)
        assert isinstance(result, FailureResult)
        assert result.code == OUT_OF_RANGE_CODE
        assert result.message == OUT_OF_RANGE_MESSAGE

    def test_u_in_04b_seventeen_returns_e004(self) -> None:
        validator = InputValidator()
        result = validator.validate(GRID_SEVENTEEN)
        assert isinstance(result, FailureResult)
        assert result.code == OUT_OF_RANGE_CODE
        assert result.message == OUT_OF_RANGE_MESSAGE

    @patch(EXECUTE_PATCH)
    def test_u_in_04a_boundary_solve_raises_validation_error(
        self, execute_mock, boundary
    ) -> None:
        with pytest.raises(BoundaryValidationError) as exc_info:
            boundary.solve(GRID_MINUS_ONE)
        assert exc_info.value.code == OUT_OF_RANGE_CODE
        execute_mock.assert_not_called()

    def test_u_in_04c_bool_cell_returns_e004(self) -> None:
        validator = InputValidator()
        result = validator.validate(GRID_BOOL_TRUE)
        assert isinstance(result, FailureResult)
        assert result.code == OUT_OF_RANGE_CODE
        assert result.message == OUT_OF_RANGE_MESSAGE
